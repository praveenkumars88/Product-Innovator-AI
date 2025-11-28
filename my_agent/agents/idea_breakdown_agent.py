"""
Idea Breakdown Agent
Takes rough ideas and breaks them into structured components
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..utils.agent_helper import call_agent

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
        return """You are an Idea Breakdown Agent for a Product Innovation System.

Your task is to take a rough product idea and break it down into:
1. Problem Statement: Clear description of the problem being solved
2. Value Proposition: Why this solution is valuable
3. User Personas: 2-3 key user personas with needs
4. Proposed Features: List of MVP features
5. Constraints: Technical, business, or regulatory constraints
6. Success Metrics: How to measure success

Provide a structured breakdown that can be used for product development."""
    
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
            
            prompt = f"""Break down this product idea into structured components:

{context}

Provide:
1. Problem Statement (2-3 sentences)
2. Value Proposition (1-2 sentences)
3. User Personas (2-3 personas with names, roles, needs)
4. Proposed MVP Features (5-7 features)
5. Constraints (technical, business, regulatory)
6. Success Metrics (3-5 KPIs)"""
            
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

