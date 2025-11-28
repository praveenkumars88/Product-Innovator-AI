"""
Architecture Suggestion Agent
Generates technical blueprints for new app ideas
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..utils.agent_helper import call_agent
from ..utils.prompts import ARCHITECTURE_INSTRUCTION, ARCHITECTURE_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class ArchitectureSuggestionAgent:
    """Suggests technical architecture for products"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='architecture_suggestion_agent',
            description='Suggests technical architecture for products',
            instruction=self._get_instruction()
        )
        logger.info("ArchitectureSuggestionAgent initialized")
    
    def _get_instruction(self) -> str:
        return ARCHITECTURE_INSTRUCTION
    
    async def suggest(self, idea_context: Dict[str, Any], features: List[str] = None) -> Dict[str, Any]:
        """
        Suggest architecture for a product idea
        
        Args:
            idea_context: Context about the product idea
            features: List of features to support
            
        Returns:
            Architecture suggestion with services, databases, APIs, etc.
        """
        logger.info("Suggesting architecture", features_count=len(features) if features else 0)
        
        try:
            context = f"Product Idea: {idea_context.get('original_idea', 'N/A')}\n"
            context += f"Problem: {idea_context.get('problem_statement', 'N/A')}\n"
            if features:
                context += f"\nFeatures to Support:\n"
                for i, feature in enumerate(features, 1):
                    context += f"{i}. {feature}\n"
            
            prompt = ARCHITECTURE_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "system_architecture": "",
                "core_services": [],
                "database_design": {},
                "api_design": {},
                "third_party_integrations": [],
                "technology_stack": {},
                "scalability_considerations": [],
                "security_considerations": [],
                "deployment_strategy": "",
                "raw_architecture": str(response)
            }
            
            logger.info("Architecture suggestion completed")
            return result
            
        except Exception as e:
            logger.error("Architecture suggestion failed", error=str(e))
            return {
                "error": str(e)
            }

