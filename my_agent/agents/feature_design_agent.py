"""
Feature Design Agent
Designs features for existing applications
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..utils.agent_helper import call_agent
from ..utils.prompts import FEATURE_DESIGN_INSTRUCTION, FEATURE_DESIGN_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class FeatureDesignAgent:
    """Designs features for existing applications"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='feature_design_agent',
            description='Designs features for existing applications',
            instruction=self._get_instruction()
        )
        logger.info("FeatureDesignAgent initialized")
    
    def _get_instruction(self) -> str:
        return FEATURE_DESIGN_INSTRUCTION
    
    async def design(self, app_name: str, feature_request: str, existing_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Design a feature for an existing app
        
        Args:
            app_name: Name of the existing application
            feature_request: Description of the feature to add
            existing_context: Optional context about the existing app
            
        Returns:
            Feature design with epics, user stories, acceptance criteria, etc.
        """
        logger.info("Designing feature", app=app_name, feature=feature_request)
        
        try:
            context = f"App: {app_name}\nFeature Request: {feature_request}\n\n"
            if existing_context:
                context += f"Existing Context: {existing_context}\n"
            
            prompt = FEATURE_DESIGN_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "app_name": app_name,
                "feature_request": feature_request,
                "feature_overview": "",
                "user_journey": [],
                "epics": [],
                "user_stories": [],
                "acceptance_criteria": {},
                "ux_impact": "",
                "integration_points": [],
                "technical_considerations": [],
                "backward_compatibility": "",
                "raw_design": str(response)
            }
            
            logger.info("Feature design completed", app=app_name)
            return result
            
        except Exception as e:
            logger.error("Feature design failed", error=str(e), app=app_name)
            return {
                "app_name": app_name,
                "feature_request": feature_request,
                "error": str(e)
            }

