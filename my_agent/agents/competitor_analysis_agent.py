"""
Competitor Analysis Agent
Researches competitors and identifies differentiation opportunities
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..tools.google_search import google_search
from ..utils.agent_helper import call_agent
from ..utils.prompts import COMPETITOR_ANALYSIS_INSTRUCTION, COMPETITOR_ANALYSIS_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class CompetitorAnalysisAgent:
    """Analyzes competitors and identifies differentiation"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='competitor_analysis_agent',
            description='Analyzes competitors and market positioning',
            instruction=self._get_instruction()
        )
        logger.info("CompetitorAnalysisAgent initialized")
    
    def _get_instruction(self) -> str:
        return COMPETITOR_ANALYSIS_INSTRUCTION
    
    async def analyze(self, domain: str, product_type: str, idea_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze competitors
        
        Args:
            domain: Domain name
            product_type: Type of product
            idea_context: Optional context about the idea/product
            
        Returns:
            Competitor analysis with top players, feature comparison, gaps
        """
        logger.info("Analyzing competitors", domain=domain, product_type=product_type)
        
        try:
            # Search for competitors
            competitor_results = await google_search.search_competitors(domain, product_type)
            
            # Build context
            context = f"Domain: {domain}\nProduct Type: {product_type}\n\n"
            if idea_context:
                context += f"Idea Context: {idea_context}\n\n"
            if competitor_results:
                context += "Competitor Search Results:\n"
                for i, result in enumerate(competitor_results[:5], 1):
                    context += f"{i}. {result.get('title', '')}\n   {result.get('snippet', '')}\n\n"
            
            prompt = COMPETITOR_ANALYSIS_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "domain": domain,
                "product_type": product_type,
                "top_competitors": [],
                "feature_comparison": {},
                "market_gaps": [],
                "differentiation_opportunities": [],
                "pricing_models": {},
                "market_positioning": {},
                "raw_analysis": str(response)
            }
            
            logger.info("Competitor analysis completed", domain=domain)
            return result
            
        except Exception as e:
            logger.error("Competitor analysis failed", error=str(e), domain=domain)
            return {
                "domain": domain,
                "product_type": product_type,
                "error": str(e)
            }

