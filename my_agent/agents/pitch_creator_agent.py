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

Your task is to create compelling visual pitch deck slides in Marp format (Markdown Presentation).

Each slide should be:
- Visually appealing with clear structure
- Concise (3-5 bullet points max per slide)
- Use appropriate slide titles
- Include visual elements descriptions where helpful

Format: Use Marp slide format with --- separator between slides.
Each slide should have a clear title and focused content."""
    
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
            
            prompt = f"""Create a compelling visual pitch deck in Marp format (Markdown Presentation) for this product:

{context}

Create 8-10 slides using Marp format. Use --- to separate slides.

Slide Structure:
1. Title Slide: Product/Feature Name + Tagline
2. The Problem: Clear pain points (3-4 bullets)
3. The Solution: What you're building (3-4 bullets)
4. Key Features: Top 4-5 features (bullet format)
5. Market Opportunity: TAM/SAM/SOM with numbers
6. Competitive Advantage: Why you'll win (3-4 points)
7. Business Model: Revenue streams (clear bullets)
8. Traction/Milestones: If applicable
9. Ask/Next Steps: What you need (call to action)
10. Closing: Memorable closing statement

Format Requirements:
- Use --- to separate each slide
- Each slide starts with # Title
- Use bullet points (• or -)
- Keep text concise (3-5 bullets per slide max)
- Use **bold** for emphasis
- Add visual descriptions in parentheses where helpful (e.g., "Chart showing growth", "Icon representing feature")

Example format:
---
# Slide Title

• Key point 1
• Key point 2
• Key point 3

---

Write in engaging, persuasive startup pitch style suitable for investors or stakeholders. Make it visual and impactful."""
            
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

