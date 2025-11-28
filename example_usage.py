"""
Example Usage of MAPIS
Demonstrates how to use the Multi-Agent Product Innovation System
"""
import asyncio
from my_agent.orchestrator import MAPISOrchestrator


async def example_new_app_idea():
    """Example: New App Idea"""
    print("\n" + "="*60)
    print("EXAMPLE 1: New App Idea")
    print("="*60)
    
    orchestrator = MAPISOrchestrator()
    user_input = "Give me a new idea in the EdTech domain"
    
    result = await orchestrator.process(user_input, session_id="example_1")
    
    print(f"\nIntent: {result.get('intent')}")
    print(f"Domain: {result.get('domain')}")
    print(f"Status: {result.get('status')}")
    
    if result.get('idea_breakdown'):
        print("\nIdea Breakdown:")
        print(f"  Problem: {result['idea_breakdown'].get('problem_statement', 'N/A')[:100]}...")
    
    if result.get('market_size'):
        print("\nMarket Size:")
        tam = result['market_size'].get('tam', {}).get('value_usd', 0)
        print(f"  TAM: ${tam:,}")


async def example_feature_extension():
    """Example: Feature Extension"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Feature Extension")
    print("="*60)
    
    orchestrator = MAPISOrchestrator()
    user_input = "Add a voice ordering feature for Swiggy"
    
    result = await orchestrator.process(user_input, session_id="example_2")
    
    print(f"\nIntent: {result.get('intent')}")
    print(f"Status: {result.get('status')}")
    
    if result.get('feature_design'):
        print("\nFeature Design:")
        print(f"  App: {result['feature_design'].get('app_name', 'N/A')}")
        print(f"  Feature: {result['feature_design'].get('feature_request', 'N/A')[:100]}...")
    
    if result.get('concept_paper'):
        print("\nConcept Paper Generated: Yes")


async def main():
    """Run examples"""
    print("MAPIS - Example Usage")
    print("="*60)
    
    # Example 1: New App Idea
    await example_new_app_idea()
    
    # Example 2: Feature Extension
    await example_feature_extension()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())

