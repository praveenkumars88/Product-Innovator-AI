"""
Main Entry Point for MAPIS
Multi-Agent Product Innovation System
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Get the project root directory (where this file is located)
project_root = Path(__file__).parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Verify API key is loaded (for debugging)
if not os.getenv('GOOGLE_API_KEY'):
    print("Warning: GOOGLE_API_KEY not found in environment variables.")
    print(f"Looking for .env file at: {env_path}")
    if not env_path.exists():
        print(f".env file not found at {env_path}")
    print("Please ensure GOOGLE_API_KEY is set in your .env file.")
    print()

from my_agent.orchestrator import MAPISOrchestrator
from my_agent.memory import session_service
from my_agent.utils.logger import logger
from my_agent.utils.file_output import save_outputs_to_files


async def main():
    """Main function to run MAPIS"""
    print("=" * 60)
    print("Multi-Agent Product Innovation System (MAPIS)")
    print("=" * 60)
    print()
    
    orchestrator = MAPISOrchestrator()
    
    # Example usage
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        print("Enter your product idea or feature request:")
        print("Examples:")
        print("  - 'Give me a new idea in the EdTech domain'")
        print("  - 'Add a voice ordering feature for Swiggy'")
        print()
        print("(Paste your message and press Enter to start processing)")
        print()
        
        # Wait for user input - input() already waits for Enter key
        user_input = input("Your input: ").strip()
        
        # Check if input was provided
        if not user_input:
            print("\nNo input provided. Exiting.")
            return
        
        # Confirm processing will start
        print(f"\n✓ Input received. Starting processing...")
        print(f"Processing: {user_input[:100]}{'...' if len(user_input) > 100 else ''}\n")
        print("-" * 60)
    
    try:
        # Process the request
        result = await orchestrator.process(user_input, session_id="session_1")
        
        # Display results
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        if result.get("status") == "error":
            print(f"Error: {result.get('error')}")
            return
        
        # Display summary
        summary = result.get("summary", {})
        print(f"\nIntent: {summary.get('intent', 'N/A')}")
        print(f"Domain: {result.get('domain', 'N/A')}")
        print(f"Agents Executed: {summary.get('agents_executed', 0)}")
        print(f"Has Wireframes: {summary.get('has_wireframes', False)}")
        print(f"Has Architecture: {summary.get('has_architecture', False)}")
        print(f"Has Market Data: {summary.get('has_market_data', False)}")
        
        # Display key outputs based on intent
        intent = result.get("intent")
        
        if intent == "new_app_idea":
            print("\n--- IDEA BREAKDOWN ---")
            idea = result.get("idea_breakdown", {})
            print(f"Problem: {idea.get('problem_statement', 'N/A')[:200]}...")
            print(f"Value Prop: {idea.get('value_proposition', 'N/A')[:200]}...")
            
            print("\n--- MARKET SIZE ---")
            market = result.get("market_size", {})
            tam = market.get("tam", {}).get("value_usd", 0)
            sam = market.get("sam", {}).get("value_usd", 0)
            print(f"TAM: ${tam:,}")
            print(f"SAM: ${sam:,}")
            
            print("\n--- PITCH ---")
            pitch = result.get("pitch", {}).get("full_text", "")
            print(pitch[:500] + "..." if len(pitch) > 500 else pitch)
        
        elif intent == "feature_extension":
            print("\n--- FEATURE DESIGN ---")
            feature = result.get("feature_design", {})
            print(f"Feature: {feature.get('feature_request', 'N/A')}")
            print(f"Overview: {feature.get('feature_overview', 'N/A')[:200]}...")
            
            print("\n--- CONCEPT PAPER ---")
            concept = result.get("concept_paper", {}).get("full_text", "")
            print(concept[:500] + "..." if len(concept) > 500 else concept)
        
        # Save outputs to files
        print("\n" + "=" * 60)
        print("Saving outputs to files...")
        saved_files = save_outputs_to_files(result, session_id="session_1")
        
        if saved_files:
            print(f"\n✓ Saved {len(saved_files)} output files:")
            for output_type, file_path in saved_files.items():
                if output_type != "complete_results":  # Don't show JSON file in summary
                    print(f"  - {output_type.replace('_', ' ').title()}: {file_path}")
            print(f"\nAll files saved to: {Path(saved_files.get('readme', '')).parent if saved_files.get('readme') else 'outputs/'}")
        else:
            print("⚠ No files were saved.")
        
        print("\n" + "=" * 60)
        print("Full results saved to session memory and files.")
        print("=" * 60)
        
    except Exception as e:
        logger.error("Main execution failed", error=str(e))
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

