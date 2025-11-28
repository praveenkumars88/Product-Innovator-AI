"""
Domain Understanding Agent
Analyzes domain, identifies pain points, user segments, trends, and market gaps
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..tools.google_search import google_search
from ..utils.agent_helper import call_agent

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
        return """You are a Domain Understanding Agent for a Product Innovation System.

Your task is to analyze a given domain and provide:
1. Pain Points: Key problems users face in this domain
2. User Segments: Different types of users/customers
3. Trends: Current and emerging trends
4. Market Gaps: Opportunities for new products/features
5. Key Players: Major companies/products in this space

Provide a comprehensive analysis in a structured format."""
    
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
            
            prompt = f"""Analyze the {domain} domain and provide:
1. Top 5 pain points users face
2. 3-5 key user segments
3. Current trends (2024-2025)
4. Market gaps and opportunities
5. Key players in this space

{context}"""
            
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

