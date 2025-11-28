"""
Concept Paper Writer Agent
Generates enterprise-style concept papers
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..utils.agent_helper import call_agent

logger = structlog.get_logger(__name__)


class ConceptPaperWriterAgent:
    """Writes enterprise-style concept papers"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='concept_paper_writer_agent',
            description='Writes enterprise-style concept papers',
            instruction=self._get_instruction()
        )
        logger.info("ConceptPaperWriterAgent initialized")
    
    def _get_instruction(self) -> str:
        return """You are a Concept Paper Writer Agent for a Product Innovation System.

Your task is to write comprehensive enterprise-style concept papers with:
1. Executive Summary
2. Background
3. Problem Statement
4. Personas
5. Proposed Solution
6. User Journeys
7. Technical Overview
8. KPIs
9. Risks & Mitigation
10. Rollout Plan
11. Open Questions

Write in professional, enterprise-grade format."""
    
    async def write(self, feature_context: Dict[str, Any], app_name: str = None) -> Dict[str, Any]:
        """
        Write a concept paper
        
        Args:
            feature_context: Context about the feature/product
            app_name: Optional app name (for feature extensions)
            
        Returns:
            Complete concept paper with all sections
        """
        logger.info("Writing concept paper", app=app_name)
        
        try:
            context = ""
            if app_name:
                context += f"Application: {app_name}\n"
            if feature_context.get("feature_request"):
                context += f"Feature: {feature_context['feature_request']}\n"
            if feature_context.get("feature_overview"):
                context += f"Overview: {feature_context['feature_overview']}\n"
            if feature_context.get("user_stories"):
                context += f"\nUser Stories:\n"
                for story in feature_context['user_stories'][:5]:
                    context += f"- {story}\n"
            
            prompt = f"""Write a concise, well-structured concept paper for this feature/product:

{context}

Requirements:
- Keep each section concise and focused
- Use bullet points where appropriate
- Avoid overly long paragraphs (max 3-4 sentences per paragraph)
- Be clear and direct, avoid unnecessary verbosity

Include all sections:
1. Executive Summary (2-3 concise paragraphs summarizing the key points)
2. Background (brief context, 1-2 paragraphs)
3. Problem Statement (clear, bulleted list of problems)
4. Personas (2-3 key personas, brief descriptions with key points)
5. Proposed Solution (structured solution with key components as bullets)
6. User Journeys (concise step-by-step flows, use numbered lists)
7. Technical Overview (high-level architecture, key integrations, bullet format)
8. KPIs (key performance indicators as a bulleted list)
9. Risks & Mitigation (brief table or bullet list format)
10. Rollout Plan (phased approach with clear phases)
11. Open Questions (brief list of unresolved items)

Write in professional, enterprise-grade format but keep it concise and scannable. Use formatting (bullets, numbered lists, tables) to improve readability."""
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "concept_paper": {
                    "executive_summary": "",
                    "background": "",
                    "problem_statement": "",
                    "personas": [],
                    "proposed_solution": "",
                    "user_journeys": [],
                    "technical_overview": "",
                    "kpis": [],
                    "risks_mitigation": {},
                    "rollout_plan": [],
                    "open_questions": []
                },
                "full_text": str(response),
                "app_name": app_name
            }
            
            logger.info("Concept paper written", app=app_name)
            return result
            
        except Exception as e:
            logger.error("Concept paper writing failed", error=str(e))
            return {
                "error": str(e),
                "concept_paper": {}
            }

