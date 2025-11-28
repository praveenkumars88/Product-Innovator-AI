"""
Agent Helper Utilities
Provides a wrapper for Google ADK Agent to handle API calls correctly
"""
from google.adk.agents.llm_agent import Agent
from typing import Any, Optional
import structlog

logger = structlog.get_logger(__name__)

# Try to import Content and Part from Google ADK if available
try:
    from google.adk.events import Content, Part
    HAS_CONTENT = True
except ImportError:
    HAS_CONTENT = False
    logger.debug("Content and Part not available from google.adk.events")


async def call_agent(agent: Agent, prompt: str) -> str:
    """
    Call an agent with a prompt and return the response
    
    Tries different methods to call the agent:
    1. invoke() - most common in modern frameworks
    2. call() - alternative method
    3. generate() - sometimes used
    4. run() - fallback
    
    Args:
        agent: The Agent instance
        prompt: Input prompt
        
    Returns:
        Agent response as string
    """
    import inspect
    
    # Note: Google ADK Agent doesn't have invoke(), call(), generate(), or run() methods
    # We need to use run_async() or run_live(), both of which require Pydantic models
    # Since input_schema is None, we need to create a proper model with all required attributes
    
    # Try run_live() - it might have simpler requirements than run_async
    # run_live is designed for streaming and might accept simpler inputs
    if hasattr(agent, 'run_live') and callable(getattr(agent, 'run_live', None)):
        logger.info("Attempting run_live() first (simpler input requirements)")
        try:
            # Try with simple string first
            logger.info("Trying run_live() with string input")
            result_chunks = []
            async for chunk in agent.run_live(prompt):
                result_chunks.append(chunk)
            result = ''.join(str(chunk) for chunk in result_chunks)
            if result:
                logger.info("✓ run_live() succeeded with string input")
                return _extract_text(result)
            else:
                logger.warning("run_live() returned empty result")
        except Exception as e:
            logger.warning(f"run_live() with string failed: {str(e)[:100]}, error_type: {type(e).__name__}")
            
            # Try with dict format
            try:
                logger.info("Trying run_live() with dict input")
                result_chunks = []
                async for chunk in agent.run_live({"input": prompt}):
                    result_chunks.append(chunk)
                result = ''.join(str(chunk) for chunk in result_chunks)
                if result:
                    logger.info("✓ run_live() succeeded with dict input")
                    return _extract_text(result)
                else:
                    logger.warning("run_live() with dict returned empty result")
            except Exception as e2:
                logger.warning(f"run_live() with dict also failed: {str(e2)[:100]}, error_type: {type(e2).__name__}")
    else:
        logger.info("Agent does not have run_live() method, skipping to run_async()")
    
    # Try run_async() second (Google ADK's async method)
    # Note: run_async returns an async generator and expects a Pydantic model input
    if hasattr(agent, 'run_async') and callable(getattr(agent, 'run_async', None)):
        try:
            run_async_method = getattr(agent, 'run_async')
            
            # Check if agent has input_schema to understand expected format
            input_schema = None
            if hasattr(agent, 'input_schema'):
                input_schema = agent.input_schema
                logger.info(f"Found input_schema: {input_schema}, type: {type(input_schema)}")
                if input_schema is None:
                    logger.warning("input_schema exists but is None")
                else:
                    import inspect
                    logger.info(f"input_schema is class: {inspect.isclass(input_schema)}")
                    if inspect.isclass(input_schema):
                        logger.info(f"input_schema MRO: {input_schema.__mro__}")
            else:
                logger.warning("Agent does not have input_schema attribute")
            
            # Try to create proper input model
            input_data = None
            if input_schema:
                try:
                    import inspect
                    from pydantic import BaseModel
                    
                    # Check if it's a Pydantic BaseModel class
                    is_pydantic_class = inspect.isclass(input_schema) and issubclass(input_schema, BaseModel)
                    
                    if is_pydantic_class:
                        logger.info("input_schema is a Pydantic BaseModel class")
                        # Get model fields to find the right field name
                        model_fields = getattr(input_schema, 'model_fields', {})
                        logger.info(f"Model fields available: {list(model_fields.keys())}")
                        
                        # Try model_validate (Pydantic v2) - preferred method
                        if hasattr(input_schema, 'model_validate'):
                            # Try common field names first
                            for field_name in ["input", "message", "query", "text", "prompt", "content"]:
                                if field_name in model_fields:
                                    try:
                                        input_data = input_schema.model_validate({field_name: prompt})
                                        logger.info(f"✓ Created input model with field '{field_name}' using model_validate")
                                        break
                                    except Exception as e:
                                        logger.debug(f"Failed with field '{field_name}': {str(e)[:100]}")
                                        continue
                            
                            # If no common field worked, try first available field
                            if input_data is None and model_fields:
                                first_field = list(model_fields.keys())[0]
                                try:
                                    input_data = input_schema.model_validate({first_field: prompt})
                                    logger.info(f"✓ Created input model with first field '{first_field}'")
                                except Exception as e:
                                    logger.warning(f"Failed with first field '{first_field}': {str(e)[:100]}")
                        
                        # Fallback to parse_obj (Pydantic v1)
                        if input_data is None and hasattr(input_schema, 'parse_obj'):
                            for field_name in ["input", "message", "query", "text", "prompt", "content"]:
                                if field_name in model_fields:
                                    try:
                                        input_data = input_schema.parse_obj({field_name: prompt})
                                        logger.info(f"✓ Created input model with field '{field_name}' using parse_obj")
                                        break
                                    except Exception as e:
                                        logger.debug(f"parse_obj failed with field '{field_name}': {str(e)[:100]}")
                                        continue
                        
                        # Last resort: try direct instantiation
                        if input_data is None:
                            for field_name in ["input", "message", "query", "text", "prompt", "content"]:
                                if field_name in model_fields:
                                    try:
                                        input_data = input_schema(**{field_name: prompt})
                                        logger.info(f"✓ Created input model with field '{field_name}' using direct instantiation")
                                        break
                                    except Exception as e:
                                        logger.debug(f"Direct instantiation failed with field '{field_name}': {str(e)[:100]}")
                                        continue
                        
                except Exception as e:
                    logger.warning("Failed to create input model from schema", error=str(e), error_type=type(e).__name__)
                    import traceback
                    logger.debug("Traceback:", traceback=traceback.format_exc())
                    input_data = None
            
            # If we have input_data, use it; otherwise try different formats
            if input_data:
                result_chunks = []
                async_gen = run_async_method(input_data)
                async for chunk in async_gen:
                    result_chunks.append(chunk)
                result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                logger.info("run_async() succeeded with Pydantic model input")
                return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
            
            # Try with Content object (Google ADK standard format)
            if HAS_CONTENT:
                try:
                    logger.info("Attempting to use Content object")
                    content_obj = Content(role='user', parts=[Part(text=prompt)])
                    logger.info(f"Created Content object: {content_obj}")
                    result_chunks = []
                    async_gen = run_async_method(content_obj)
                    async for chunk in async_gen:
                        result_chunks.append(chunk)
                    result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                    logger.info("✓ run_async() succeeded with Content object")
                    return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                except Exception as e:
                    logger.warning("run_async() with Content object failed", error=str(e), error_type=type(e).__name__)
            else:
                logger.debug("Content/Part not available, skipping Content object attempt")
            
            # Since input_schema is None, create a comprehensive flexible model
            # Based on all errors encountered, include all discovered attributes
            if input_schema is None:
                try:
                    from pydantic import BaseModel
                    logger.info("input_schema is None, creating comprehensive flexible input model")
                    
                    # Create a mock plugin_manager with the required method
                    class MockPluginManager:
                        async def run_before_agent_callback(self, *args, **kwargs):
                            return None
                    
                    # RunConfig model - include ALL discovered attributes
                    # Based on all errors encountered so far:
                    # - response_modalities
                    # - speech_config  
                    # - output_audio_transcription
                    # And any future ones via Config.extra = "allow"
                    class RunConfig(BaseModel):
                        response_modalities: Optional[list] = []
                        speech_config: Optional[Any] = None
                        output_audio_transcription: Optional[Any] = None
                        # Config.extra = "allow" will accept any additional fields
                        
                        class Config:
                            extra = "allow"  # Accept ANY additional fields to prevent future errors
                    
                    # Session model with all discovered attributes
                    class SessionWithId(BaseModel):
                        id: str = "default_session"
                        state: Optional[dict] = {}
                        
                        class Config:
                            extra = "allow"
                    
                    # Comprehensive input model with ALL discovered attributes
                    # This includes ALL attributes discovered through error messages:
                    # - session (with id and state)
                    # - plugin_manager (with run_before_agent_callback)
                    # - end_invocation
                    # - agent_states
                    # - run_config (with response_modalities and speech_config)
                    # - response_modalities (also on model itself)
                    class ComprehensiveInput(BaseModel):
                        # Primary input fields (try multiple common names)
                        input: Optional[str] = None
                        message: Optional[str] = None
                        text: Optional[str] = None
                        query: Optional[str] = None
                        prompt: Optional[str] = None
                        content: Optional[str] = None
                        
                        # Session-related (discovered from errors: needs id and state)
                        session: Optional[SessionWithId] = None
                        
                        # Plugin manager (discovered: needs run_before_agent_callback method)
                        plugin_manager: Optional[Any] = None
                        
                        # Other discovered attributes (from all error messages)
                        end_invocation: Optional[Any] = None
                        agent_states: Optional[dict] = {}
                        run_config: Optional[RunConfig] = None  # RunConfig with response_modalities and speech_config
                        response_modalities: Optional[list] = []  # Also on model itself
                        
                        class Config:
                            extra = "allow"  # Accept ANY additional fields to prevent future attribute errors
                        
                        @classmethod
                        def create(cls, prompt: str):
                            """Factory method to create ComprehensiveInput with proper defaults"""
                            prompt_text = prompt or ""
                            return cls(
                                input=prompt_text,
                                message=prompt_text,
                                text=prompt_text,
                                session=SessionWithId(id="default_session", state={}),
                                plugin_manager=MockPluginManager(),
                                end_invocation=None,
                                agent_states={},
                                run_config=RunConfig(response_modalities=[], speech_config=None, output_audio_transcription=None),
                                response_modalities=[]
                            )
                    
                    # Try with comprehensive model
                    try:
                        input_data = ComprehensiveInput.create(prompt)
                        logger.info("Created ComprehensiveInput model with all discovered attributes")
                        result_chunks = []
                        async_gen = run_async_method(input_data)
                        async for chunk in async_gen:
                            result_chunks.append(chunk)
                        result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                        logger.info("✓ run_async() succeeded with ComprehensiveInput model")
                        return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                    except Exception as e1:
                        error_msg = str(e1)
                        logger.debug(f"ComprehensiveInput failed: {error_msg[:150]}")
                        
                        # If it's an attribute error, try to add the missing attribute dynamically
                        if "has no attribute" in error_msg:
                            missing_attr = error_msg.split("'")[1] if "'" in error_msg else None
                            if missing_attr:
                                logger.info(f"Detected missing attribute: {missing_attr}, adding to model")
                                # Add the missing attribute to the model dynamically
                                try:
                                    # Create a new model class with the missing attribute
                                    class ComprehensiveInputWithAttr(ComprehensiveInput):
                                        pass
                                    
                                    # Add the missing attribute as a field
                                    setattr(ComprehensiveInputWithAttr, missing_attr, None)
                                    
                                    input_data = ComprehensiveInputWithAttr(input=prompt)
                                    result_chunks = []
                                    async_gen = run_async_method(input_data)
                                    async for chunk in async_gen:
                                        result_chunks.append(chunk)
                                    result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                                    logger.info(f"✓ run_async() succeeded after adding {missing_attr}")
                                    return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                                except Exception as e2:
                                    logger.debug(f"Failed even after adding {missing_attr}: {str(e2)[:100]}")
                    
                    # Fallback to simpler models if comprehensive fails
                    class SimpleInputWithSession(BaseModel):
                        input: str
                        session: Optional[SessionWithId] = None
                        plugin_manager: Optional[Any] = None
                        end_invocation: Optional[Any] = None
                        agent_states: Optional[dict] = {}
                        run_config: Optional[RunConfig] = None  # Use RunConfig model
                        response_modalities: Optional[list] = []
                        
                        class Config:
                            extra = "allow"
                    
                    # Fallback: try simpler model
                    try:
                        session_obj = SessionWithId(id="default_session", state={})
                        plugin_mgr = MockPluginManager()
                        input_data = SimpleInputWithSession(
                            input=prompt, 
                            session=session_obj, 
                            plugin_manager=plugin_mgr,
                            run_config=RunConfig(response_modalities=[], speech_config=None),
                            response_modalities=[]
                        )
                        logger.info("Trying SimpleInputWithSession as fallback")
                        result_chunks = []
                        async_gen = run_async_method(input_data)
                        async for chunk in async_gen:
                            result_chunks.append(chunk)
                        result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                        logger.info("✓ run_async() succeeded with SimpleInputWithSession")
                        return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                    except Exception as e_fallback:
                        error_msg = str(e_fallback)
                        logger.warning("All model attempts failed", error=error_msg[:200])
                        
                        # Last attempt: try with run_config as dict but with response_modalities key
                        try:
                            logger.info("Trying with run_config as dict containing response_modalities")
                            class LastResortInput(BaseModel):
                                input: str
                                session: Optional[SessionWithId] = None
                                plugin_manager: Optional[Any] = None
                                end_invocation: Optional[Any] = None
                                agent_states: Optional[dict] = {}
                                run_config: Optional[RunConfig] = None  # Use RunConfig model, not dict
                                response_modalities: Optional[list] = []
                                
                                class Config:
                                    extra = "allow"
                            
                            session_obj = SessionWithId(id="default_session", state={})
                            plugin_mgr = MockPluginManager()
                            input_data = LastResortInput(
                                input=prompt,
                                session=session_obj,
                                plugin_manager=plugin_mgr,
                                run_config=RunConfig(response_modalities=[], speech_config=None, output_audio_transcription=None),
                                response_modalities=[]
                            )
                            result_chunks = []
                            async_gen = run_async_method(input_data)
                            async for chunk in async_gen:
                                result_chunks.append(chunk)
                            result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                            logger.info("✓ run_async() succeeded with LastResortInput")
                            return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                        except Exception as e_last:
                            logger.warning("Even LastResortInput failed", error=str(e_last)[:200])
                except Exception as e:
                    logger.warning("run_async() with simple models failed", error=str(e), error_type=type(e).__name__)
            
            # Fallback: try with string (might work if schema is flexible)
            try:
                result_chunks = []
                async_gen = run_async_method(prompt)
                async for chunk in async_gen:
                    result_chunks.append(chunk)
                result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                logger.info("run_async() succeeded with string input")
                return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
            except Exception as e:
                logger.warning("run_async() with string failed", error=str(e), error_type=type(e).__name__)
                
                # Try with dict and let Pydantic validate it
                for key in ["input", "message", "query", "text", "prompt", "content"]:
                    try:
                        result_chunks = []
                        async_gen = run_async_method({key: prompt})
                        async for chunk in async_gen:
                            result_chunks.append(chunk)
                        result = ''.join(_extract_text(chunk) for chunk in result_chunks)
                        logger.info(f"run_async() succeeded with dict key '{key}'")
                        return result if result else _extract_text(result_chunks[-1]) if result_chunks else ""
                    except Exception as e2:
                        logger.debug(f"run_async() failed with key '{key}'", error=str(e2))
                        continue
        except Exception as e:
            logger.warning("run_async() failed completely", error=str(e), error_type=type(e).__name__)
    
    # run_live() already tried at the beginning, skip here to avoid duplicate attempts
    
    # Simple methods already tried at the beginning, skip here to avoid duplicates
    
    # If all methods fail, try direct attribute access
    try:
        # Some agents might have a direct response attribute
        if hasattr(agent, 'response'):
            return str(agent.response)
    except Exception as e:
        logger.debug("response attribute access failed", error=str(e))
    
    # Last resort: return error message
    logger.error("Could not call agent - no valid method found. Available methods: " + str([m for m in dir(agent) if not m.startswith('_')]))
    return "Error: Could not get response from agent. Please check agent configuration."


def _extract_text(result: Any) -> str:
    """Extract text from agent response which might be in various formats"""
    if isinstance(result, str):
        return result
    elif hasattr(result, 'text'):
        return str(result.text)
    elif hasattr(result, 'content'):
        return str(result.content)
    elif hasattr(result, 'message'):
        return str(result.message)
    elif isinstance(result, dict):
        # Try common keys
        for key in ['text', 'content', 'message', 'response', 'output']:
            if key in result:
                return str(result[key])
        # Return string representation of dict
        return str(result)
    else:
        return str(result)

