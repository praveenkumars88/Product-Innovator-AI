"""
Agent Helper Utilities
Provides a wrapper for Google ADK Agent to handle API calls correctly
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables early (before importing google modules)
# This ensures GOOGLE_API_KEY is available when Google GenAI initializes
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Try loading from current directory as fallback
    load_dotenv()

from google.adk import Runner
from google.adk.agents.llm_agent import Agent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from typing import Any, Optional
import structlog

logger = structlog.get_logger(__name__)

# Global session service instance (shared across all agents)
_session_service = InMemorySessionService()


async def call_agent(agent: Agent, prompt: str, session_id: str = "default_session", user_id: str = "default_user") -> str:
    """
    Call an agent with a prompt and return the response
    
    Uses the Google ADK Runner API which is the proper way to invoke agents.
    
    Args:
        agent: The Agent instance
        prompt: Input prompt text
        session_id: Session ID for maintaining conversation context
        user_id: User ID for the session
        
    Returns:
        Agent response as string
    """
    try:
        # Note: Runner expects app_name to match where agent class is loaded from
        # Since Agent comes from google.adk.agents, we use 'agents' to avoid warnings
        # In production, you'd want to use your actual app name
        app_name = 'agents'  # Match the package structure to avoid session lookup issues
        
        # Ensure session exists BEFORE creating Runner
        session = await _session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        if session is None:
            # Session doesn't exist, create it
            await _session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )
        
        # Create a Runner instance for this agent
        runner = Runner(
            app_name=app_name,
            agent=agent,
            session_service=_session_service
        )
        
        # Create Content object for the user message
        content = types.Content(
            role='user',
            parts=[types.Part(text=prompt)]
        )
        
        # Call the agent using Runner.run_async
        result_chunks = []
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            # Extract text from events
            text = _extract_text_from_event(event)
            if text:
                result_chunks.append(text)
        
        # Combine all chunks
        result = ''.join(result_chunks)
        
        if result:
            logger.info("Agent call successful", response_length=len(result))
            return result
        else:
            logger.warning("Agent returned empty response")
            return "Error: Agent returned empty response."
            
    except Exception as e:
        logger.error("Agent call failed", error=str(e), error_type=type(e).__name__)
        import traceback
        logger.debug("Traceback", traceback=traceback.format_exc())
        return f"Error: Could not get response from agent: {str(e)}"


def _extract_text_from_event(event: Any) -> str:
    """Extract text from a Google ADK Event object"""
    if isinstance(event, str):
        return event
    
    # Try common event attributes
    if hasattr(event, 'text'):
        return str(event.text)
    
    if hasattr(event, 'content'):
        content = event.content
        if isinstance(content, str):
            return content
        if hasattr(content, 'parts'):
            texts = []
            for part in content.parts:
                if hasattr(part, 'text'):
                    texts.append(str(part.text))
            return ''.join(texts)
    
    if hasattr(event, 'message'):
        return str(event.message)
    
    if hasattr(event, 'response'):
        return str(event.response)
    
    # Try to get text from parts if available
    if hasattr(event, 'parts'):
        texts = []
        for part in event.parts:
            if hasattr(part, 'text'):
                texts.append(str(part.text))
        if texts:
            return ''.join(texts)
    
    # Last resort: string representation
    return str(event)
