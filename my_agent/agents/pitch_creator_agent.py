"""
Pitch Creator Agent
Produces startup-style pitch summaries
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..utils.agent_helper import call_agent

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
        return """You are a Pitch Creator Agent for a Product Innovation System.

Your task is to create compelling startup-style pitch summaries with:
1. Hook (attention-grabbing opening)
2. Problem (pain point being solved)
3. Solution (your product/feature)
4. Features (key capabilities)
5. Market Size (TAM/SAM/SOM)
6. Competitive Edge (differentiation)
7. Business Model (revenue streams)
8. Closing Statement (call to action)

Write in engaging, persuasive startup pitch style."""
    
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
            context = f"Product Idea: {idea_context.get('original_idea', 'N/A')}\n"
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
            
            prompt = f"""Create a compelling startup pitch for this product:

{context}

Include all sections:
1. Hook (1-2 sentences that grab attention)
2. Problem (clear pain point, 2-3 sentences)
3. Solution (your product, 2-3 sentences)
4. Features (3-5 key features, bullet points)
5. Market Size (TAM/SAM/SOM summary)
6. Competitive Edge (why you'll win, 2-3 points)
7. Business Model (how you'll make money)
8. Closing Statement (call to action, 1-2 sentences)

Write in engaging, persuasive startup pitch style suitable for investors or stakeholders."""
            
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

