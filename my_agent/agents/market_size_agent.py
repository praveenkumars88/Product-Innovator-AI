"""
Market Size Agent
Calculates TAM, SAM, SOM for new app ideas
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any
import structlog
from ..tools.google_search import google_search
from ..utils.agent_helper import call_agent
from ..utils.prompts import MARKET_SIZE_INSTRUCTION, MARKET_SIZE_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class MarketSizeAgent:
    """Calculates market size (TAM/SAM/SOM)"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='market_size_agent',
            description='Calculates market size and opportunity',
            instruction=self._get_instruction()
        )
        logger.info("MarketSizeAgent initialized")
    
    def _get_instruction(self) -> str:
        return MARKET_SIZE_INSTRUCTION
    
    async def calculate(self, domain: str, product_type: str, region: str = "global", idea_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate market size
        
        Args:
            domain: Domain name
            product_type: Type of product
            region: Target region (default: global)
            idea_context: Optional context about the idea
            
        Returns:
            Market size calculations with TAM, SAM, SOM
        """
        logger.info("Calculating market size", domain=domain, region=region)
        
        try:
            # Search for market size data
            market_data = await google_search.search_market_size(domain, region)
            
            context = f"Domain: {domain}\nProduct Type: {product_type}\nRegion: {region}\n\n"
            if idea_context:
                context += f"Product Context: {idea_context.get('value_proposition', 'N/A')}\n\n"
            if market_data:
                context += "Market Research Data:\n"
                for result in market_data[:3]:
                    context += f"- {result.get('title', '')}: {result.get('snippet', '')}\n"
            
            prompt = MARKET_SIZE_PROMPT_TEMPLATE.format(context=context)
            
            response = await call_agent(self.agent, prompt)
            
            result = {
                "domain": domain,
                "product_type": product_type,
                "region": region,
                "tam": {
                    "value_usd": 0,
                    "methodology": "",
                    "assumptions": []
                },
                "sam": {
                    "value_usd": 0,
                    "percentage_of_tam": 0,
                    "target_segments": []
                },
                "som": {
                    "year_1_usd": 0,
                    "year_3_usd": 0,
                    "year_5_usd": 0,
                    "market_share_assumptions": "",
                    "growth_projections": []
                },
                "pricing_model": {},
                "market_growth_trends": {},
                "raw_calculation": str(response)
            }
            
            logger.info("Market size calculation completed", domain=domain)
            return result
            
        except Exception as e:
            logger.error("Market size calculation failed", error=str(e), domain=domain)
            return {
                "domain": domain,
                "error": str(e)
            }

