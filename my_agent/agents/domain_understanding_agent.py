"""
Domain Understanding Agent
Analyzes domain, identifies pain points, user segments, trends, and market gaps
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..tools.google_search import google_search
from ..utils.agent_helper import call_agent
from ..utils.prompts import DOMAIN_UNDERSTANDING_INSTRUCTION, DOMAIN_UNDERSTANDING_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class DomainUnderstandingAgent:
    """Analyzes domains for product opportunities"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='domain_understanding_agent',
            description='Analyzes domains to identify opportunities and pain points',
            instruction=self._get_instruction()
        )
        logger.info("DomainUnderstandingAgent initialized")
    
    def _get_instruction(self) -> str:
        return DOMAIN_UNDERSTANDING_INSTRUCTION
    
    async def analyze(self, domain: str, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a domain
        
        Args:
            domain: Domain name (e.g., "EdTech", "FinTech")
            keywords: Optional keywords to focus on
            
        Returns:
            Domain analysis with pain points, segments, trends, gaps
        """
        logger.info("Analyzing domain", domain=domain, keywords=keywords)
        
        try:
            # Search for market trends
            trends_results = await google_search.search_market_trends(domain)
            
            # Build context for the agent
            context = f"Domain: {domain}\n"
            if keywords:
                context += f"Keywords: {', '.join(keywords)}\n"
            if trends_results:
                context += f"\nRecent Trends:\n"
                for result in trends_results[:3]:
                    context += f"- {result.get('title', '')}: {result.get('snippet', '')}\n"
            
            prompt = DOMAIN_UNDERSTANDING_PROMPT_TEMPLATE.format(domain=domain, context=context)
            
            response = await call_agent(self.agent, prompt)
            
            # Structure the response
            result = {
                "domain": domain,
                "pain_points": [],
                "user_segments": [],
                "trends": [],
                "market_gaps": [],
                "key_players": [],
                "raw_analysis": str(response)
            }
            
            logger.info("Domain analysis completed", domain=domain)
            return result
            
        except Exception as e:
            logger.error("Domain analysis failed", error=str(e), domain=domain)
            return {
                "domain": domain,
                "pain_points": [],
                "user_segments": [],
                "trends": [],
                "market_gaps": [],
                "key_players": [],
                "error": str(e)
            }

