"""
Test script to inspect Google ADK Agent API
"""
import asyncio
from google.adk.agents.llm_agent import Agent
import inspect

async def test_agent_api():
    """Test and inspect the Agent API"""
    print("=" * 60)
    print("Google ADK Agent API Inspection")
    print("=" * 60)
    print()
    
    # Create a test agent
    agent = Agent(
        model='gemini-2.5-flash',
        name='test_agent',
        description='Test agent',
        instruction='Test instruction'
    )
    
    print("1. Agent Type:", type(agent))
    print()
    
    print("2. Checking input_schema:")
    if hasattr(agent, 'input_schema'):
        input_schema = agent.input_schema
        print(f"   - Has input_schema: {input_schema}")
        print(f"   - Type: {type(input_schema)}")
        if input_schema:
            print(f"   - Is class: {inspect.isclass(input_schema)}")
            if inspect.isclass(input_schema):
                print(f"   - MRO: {input_schema.__mro__}")
                if hasattr(input_schema, 'model_fields'):
                    print(f"   - Model fields: {list(input_schema.model_fields.keys())}")
    else:
        print("   - No input_schema attribute")
    print()
    
    print("3. Checking run_async method:")
    if hasattr(agent, 'run_async'):
        run_async = getattr(agent, 'run_async')
        print(f"   - Has run_async: {run_async}")
        print(f"   - Type: {type(run_async)}")
        print(f"   - Is callable: {callable(run_async)}")
        
        # Get signature
        try:
            sig = inspect.signature(run_async)
            print(f"   - Signature: {sig}")
            print(f"   - Parameters: {list(sig.parameters.keys())}")
            for param_name, param in sig.parameters.items():
                print(f"     * {param_name}: {param.annotation} (default: {param.default})")
        except Exception as e:
            print(f"   - Could not get signature: {e}")
        
        # Check if it's a coroutine function
        print(f"   - Is coroutine function: {inspect.iscoroutinefunction(run_async)}")
    else:
        print("   - No run_async attribute")
    print()
    
    print("4. Testing run_async with different inputs:")
    test_prompt = "Test prompt"
    
    # Try with string
    print("   a) Testing with string...")
    try:
        result = agent.run_async(test_prompt)
        print(f"      Result type: {type(result)}")
        print(f"      Is async generator: {inspect.isasyncgen(result)}")
        if inspect.isasyncgen(result):
            print("      ✓ Returns async generator")
            # Try to get first chunk
            try:
                first_chunk = await result.__anext__()
                print(f"      First chunk type: {type(first_chunk)}")
                print(f"      First chunk: {str(first_chunk)[:100]}")
            except StopAsyncIteration:
                print("      Generator is empty")
            except Exception as e:
                print(f"      Error getting chunk: {e}")
    except Exception as e:
        print(f"      ✗ Failed: {e}")
        print(f"      Error type: {type(e).__name__}")
    
    # Try with dict
    print("   b) Testing with dict...")
    try:
        result = agent.run_async({"input": test_prompt})
        print(f"      Result type: {type(result)}")
        print(f"      Is async generator: {inspect.isasyncgen(result)}")
    except Exception as e:
        print(f"      ✗ Failed: {e}")
        print(f"      Error type: {type(e).__name__}")
    
    # Try creating input model if schema exists
    if hasattr(agent, 'input_schema') and agent.input_schema:
        print("   c) Testing with Pydantic model...")
        try:
            from pydantic import BaseModel
            input_schema = agent.input_schema
            if inspect.isclass(input_schema) and issubclass(input_schema, BaseModel):
                # Try to create model
                model_fields = getattr(input_schema, 'model_fields', {})
                print(f"      Model fields: {list(model_fields.keys())}")
                
                # Try with first field
                if model_fields:
                    first_field = list(model_fields.keys())[0]
                    try:
                        if hasattr(input_schema, 'model_validate'):
                            input_model = input_schema.model_validate({first_field: test_prompt})
                            print(f"      ✓ Created model with field '{first_field}'")
                            result = agent.run_async(input_model)
                            print(f"      ✓ run_async accepted model")
                            print(f"      Result type: {type(result)}")
                        else:
                            print(f"      No model_validate method")
                    except Exception as e:
                        print(f"      ✗ Failed: {e}")
        except Exception as e:
            print(f"      ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print("Inspection complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_agent_api())

