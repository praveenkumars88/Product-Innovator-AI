"""
Architecture Suggestion Agent
Generates technical blueprints for new app ideas
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..utils.agent_helper import call_agent

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
        return """You are an Architecture Suggestion Agent for a Product Innovation System.

Your task is to design technical architecture for products. Provide:
1. System architecture (high-level components)
2. Services required (microservices, APIs, etc.)
3. Database design (data models, storage)
4. Third-party integrations
5. Scalability considerations
6. Technology stack recommendations

Provide comprehensive technical blueprints."""
    
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
            
            prompt = f"""Design technical architecture for this product:

{context}

Provide:
1. System Architecture Overview (high-level diagram description)
2. Core Services (list of microservices/modules needed)
3. Database Design (data models, storage requirements)
4. API Design (key endpoints, data flows)
5. Third-Party Integrations (external services, APIs, SDKs)
6. Technology Stack (recommended languages, frameworks, tools)
7. Scalability Considerations (how to handle growth)
8. Security Considerations (authentication, data protection)
9. Deployment Strategy (cloud, on-premise, hybrid)"""
            
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

