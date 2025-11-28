"""
Pitch Creator Agent
Produces startup-style pitch summaries
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..utils.agent_helper import call_agent
from ..utils.prompts import PITCH_CREATOR_INSTRUCTION, PITCH_CREATOR_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class PitchCreatorAgent:
    """Creates startup-style pitch summaries"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='pitch_creator_agent',
            description='Creates startup-style pitch summaries',
            instruction=self._get_instruction()
        )
        logger.info("PitchCreatorAgent initialized")
    
    def _get_instruction(self) -> str:
        return PITCH_CREATOR_INSTRUCTION
    
    async def create(self, idea_context: Dict[str, Any], market_data: Dict[str, Any] = None, competitor_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a pitch summary
        
        Args:
            idea_context: Context about the product idea
            market_data: Optional market size data
            competitor_data: Optional competitor analysis
            
        Returns:
            Pitch summary with all sections
        """
        logger.info("Creating pitch")
        
        try:
            # Handle both new app ideas and feature extensions
            context = ""
            
            # For feature extensions
            if idea_context.get('feature_request'):
                context += f"Feature: {idea_context.get('feature_request', 'N/A')}\n"
                context += f"App: {idea_context.get('app_name', 'N/A')}\n"
                if idea_context.get('feature_overview'):
                    context += f"Overview: {idea_context.get('feature_overview', '')}\n"
                if idea_context.get('raw_design'):
                    # Extract key points from raw_design
                    raw_design = idea_context.get('raw_design', '')
                    context += f"\nFeature Details: {raw_design[:500]}...\n"
            else:
                # For new app ideas
                context += f"Product Idea: {idea_context.get('original_idea', 'N/A')}\n"
                context += f"Problem: {idea_context.get('problem_statement', 'N/A')}\n"
                context += f"Value Proposition: {idea_context.get('value_proposition', 'N/A')}\n"
            
            if market_data:
                context += f"\nMarket Size:\n"
                if market_data.get('tam'):
                    context += f"TAM: ${market_data['tam'].get('value_usd', 0):,}\n"
                if market_data.get('sam'):
                    context += f"SAM: ${market_data['sam'].get('value_usd', 0):,}\n"
            
            if competitor_data:
                context += f"\nCompetitive Edge:\n"
                if competitor_data.get('differentiation_opportunities'):
                    for opp in competitor_data['differentiation_opportunities'][:3]:
                        context += f"- {opp}\n"
                elif competitor_data.get('raw_analysis'):
                    # Extract key differentiation points from raw_analysis
                    raw_analysis = competitor_data.get('raw_analysis', '')
                    context += f"Differentiation: {raw_analysis[:300]}...\n"
            
            prompt = PITCH_CREATOR_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "pitch": {
                    "hook": "",
                    "problem": "",
                    "solution": "",
                    "features": [],
                    "market_size": "",
                    "competitive_edge": "",
                    "business_model": "",
                    "closing_statement": ""
                },
                "full_text": str(response)
            }
            
            logger.info("Pitch created")
            return result
            
        except Exception as e:
            logger.error("Pitch creation failed", error=str(e))
            return {
                "error": str(e),
                "pitch": {}
            }

