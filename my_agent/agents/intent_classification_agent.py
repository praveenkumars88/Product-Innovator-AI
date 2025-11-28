"""
Intent Classification Agent
Determines whether user wants new app idea or feature extension
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import json
import structlog
from ..utils.agent_helper import call_agent
from ..utils.prompts import INTENT_CLASSIFICATION_INSTRUCTION

logger = structlog.get_logger(__name__)


class IntentClassificationAgent:
    """Classifies user intent: new_app_idea or feature_extension"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='intent_classification_agent',
            description='Classifies user intent for product innovation requests',
            instruction=self._get_instruction()
        )
        logger.info("IntentClassificationAgent initialized")
    
    def _get_instruction(self) -> str:
        return INTENT_CLASSIFICATION_INSTRUCTION
    
    async def classify(self, user_input: str) -> Dict[str, Any]:
        """
        Classify user intent
        
        Args:
            user_input: User's request text
            
        Returns:
            Classification result with intent, domain, keywords
        """
        logger.info("Classifying user intent", input_length=len(user_input))
        
        try:
            # Use the agent to classify
            response = await call_agent(self.agent, user_input)
            
            # Parse JSON response
            # In ADK, response might be in different format, adjust accordingly
            if isinstance(response, str):
                # Try to extract JSON from response
                response_text = response
            else:
                response_text = str(response)
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
            else:
                # Fallback: create default structure
                result = {
                    "intent": "new_app_idea",
                    "domain": None,
                    "keywords": [],
                    "confidence": 0.5
                }
            
            logger.info("Intent classified", intent=result.get("intent"), domain=result.get("domain"))
            return result
            
        except Exception as e:
            logger.error("Intent classification failed", error=str(e))
            # Return default fallback
            return {
                "intent": "new_app_idea",
                "domain": None,
                "keywords": user_input.split()[:5],
                "confidence": 0.3
            }

