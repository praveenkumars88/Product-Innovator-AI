"""
Idea Breakdown Agent
Takes rough ideas and breaks them into structured components
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..utils.agent_helper import call_agent
from ..utils.prompts import IDEA_BREAKDOWN_INSTRUCTION, IDEA_BREAKDOWN_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class IdeaBreakdownAgent:
    """Breaks down rough ideas into structured components"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='idea_breakdown_agent',
            description='Breaks down product ideas into structured components',
            instruction=self._get_instruction()
        )
        logger.info("IdeaBreakdownAgent initialized")
    
    def _get_instruction(self) -> str:
        return IDEA_BREAKDOWN_INSTRUCTION
    
    async def breakdown(self, idea: str, domain_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Break down an idea into structured components
        
        Args:
            idea: Rough product idea
            domain_context: Optional domain analysis context
            
        Returns:
            Structured breakdown with problem, value prop, personas, features, etc.
        """
        logger.info("Breaking down idea", idea_length=len(idea))
        
        try:
            context = f"Idea: {idea}\n\n"
            if domain_context:
                context += f"Domain Context:\n"
                if domain_context.get("pain_points"):
                    context += f"Pain Points: {', '.join(domain_context['pain_points'][:3])}\n"
                if domain_context.get("user_segments"):
                    context += f"User Segments: {', '.join(domain_context['user_segments'][:3])}\n"
            
            prompt = IDEA_BREAKDOWN_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "original_idea": idea,
                "problem_statement": "",
                "value_proposition": "",
                "user_personas": [],
                "proposed_features": [],
                "constraints": [],
                "success_metrics": [],
                "raw_breakdown": str(response)
            }
            
            logger.info("Idea breakdown completed")
            return result
            
        except Exception as e:
            logger.error("Idea breakdown failed", error=str(e))
            return {
                "original_idea": idea,
                "error": str(e)
            }

