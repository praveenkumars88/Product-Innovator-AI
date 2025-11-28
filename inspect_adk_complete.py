"""
Complete inspection of Google ADK Agent API to find exact input format
"""
import asyncio
import inspect
from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel

async def inspect_complete():
    """Complete inspection to find exact input format"""
    print("=" * 80)
    print("COMPLETE GOOGLE ADK AGENT API INSPECTION")
    print("=" * 80)
    print()
    
    # Create a test agent
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='test_agent',
        instruction='Test instruction'
    )
    
    print("1. AGENT INPUT_SCHEMA INSPECTION")
    print("-" * 80)
    if hasattr(agent, 'input_schema'):
        input_schema = agent.input_schema
        print(f"   input_schema value: {input_schema}")
        print(f"   input_schema type: {type(input_schema)}")
        
        if input_schema is None:
            print("\n   ⚠️  input_schema is None - need to find default format")
        elif inspect.isclass(input_schema):
            print(f"\n   ✓ input_schema is a class: {input_schema.__name__}")
            print(f"   MRO: {input_schema.__mro__}")
            
            if hasattr(input_schema, 'model_fields'):
                print(f"   Model fields: {list(input_schema.model_fields.keys())}")
                for field_name, field_info in input_schema.model_fields.items():
                    print(f"     - {field_name}: {field_info.annotation} (required: {field_info.is_required()})")
    else:
        print("   ⚠️  No input_schema attribute")
    print()
    
    print("2. RUN_ASYNC METHOD INSPECTION")
    print("-" * 80)
    if hasattr(agent, 'run_async'):
        run_async = agent.run_async
        sig = inspect.signature(run_async)
        print(f"   Signature: {sig}")
        print(f"   Parameters:")
        for param_name, param in sig.parameters.items():
            print(f"     - {param_name}: {param.annotation} (default: {param.default})")
    print()
    
    print("3. TESTING WITH DIFFERENT INPUT FORMATS")
    print("-" * 80)
    test_prompt = "Hello, test prompt"
    
    # Test 1: String
    print("\n   Test 1: String input")
    try:
        result = agent.run_async(test_prompt)
        print(f"      ✓ Accepted string")
        print(f"      Result type: {type(result)}")
        if inspect.isasyncgen(result):
            print(f"      ✓ Returns async generator")
            try:
                first_chunk = await result.__anext__()
                print(f"      First chunk type: {type(first_chunk)}")
                print(f"      First chunk preview: {str(first_chunk)[:150]}")
            except StopAsyncIteration:
                print("      Generator is empty")
            except Exception as e:
                print(f"      Error getting chunk: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"      ✗ Failed: {type(e).__name__}: {e}")
        print(f"      Error details: {str(e)[:200]}")
    
    # Test 2: Dict with common keys
    for key in ["input", "message", "query", "text", "prompt", "content"]:
        print(f"\n   Test 2.{key}: Dict with key '{key}'")
        try:
            result = agent.run_async({key: test_prompt})
            print(f"      ✓ Accepted dict with key '{key}'")
            print(f"      Result type: {type(result)}")
        except Exception as e:
            print(f"      ✗ Failed: {type(e).__name__}: {e}")
            if "attribute" in str(e).lower():
                print(f"      Missing attribute: {str(e)[:150]}")
    
    # Test 3: Try to find the actual expected model by inspecting source
    print("\n   Test 3: Inspecting source code")
    try:
        import google.adk.agents.llm_agent as llm_agent_module
        import os
        module_file = inspect.getfile(llm_agent_module)
        print(f"      Module file: {module_file}")
        
        # Try to read the source
        if os.path.exists(module_file):
            with open(module_file, 'r') as f:
                source = f.read()
                # Look for run_async definition
                if 'def run_async' in source or 'async def run_async' in source:
                    print(f"      ✓ Found run_async in source")
                    # Find the method
                    lines = source.split('\n')
                    for i, line in enumerate(lines):
                        if 'def run_async' in line or 'async def run_async' in line:
                            print(f"      Line {i+1}: {line.strip()}")
                            # Print next 20 lines
                            print(f"      Next 20 lines:")
                            for j in range(i+1, min(i+21, len(lines))):
                                print(f"        {j+1}: {lines[j]}")
                            break
    except Exception as e:
        print(f"      ✗ Could not inspect source: {e}")
    
    # Test 4: Try to find example usage or default input model
    print("\n   Test 4: Looking for default input models in ADK")
    try:
        import google.adk
        adk_dir = os.path.dirname(google.adk.__file__) if hasattr(google.adk, '__file__') else None
        if adk_dir:
            print(f"      ADK directory: {adk_dir}")
            # Look for common input model files
            for filename in ['input.py', 'models.py', 'schemas.py', 'types.py']:
                filepath = os.path.join(adk_dir, filename)
                if os.path.exists(filepath):
                    print(f"      ✓ Found: {filename}")
    except Exception as e:
        print(f"      ✗ Error: {e}")
    
    print()
    print("=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(inspect_complete())

