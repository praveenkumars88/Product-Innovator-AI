"""
Wireframe Generator Agent
Creates ASCII-style wireframes using Code Execution MCP
"""
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import structlog
from ..tools.code_execution import code_execution
from ..utils.agent_helper import call_agent
from ..utils.prompts import WIREFRAME_INSTRUCTION, WIREFRAME_PROMPT_TEMPLATE

logger = structlog.get_logger(__name__)


class WireframeGeneratorAgent:
    """Generates ASCII wireframes for UI screens"""
    
    def __init__(self, model: str = 'gemini-2.5-flash'):
        self.agent = Agent(
            model=model,
            name='wireframe_generator_agent',
            description='Generates wireframes for product screens',
            instruction=self._get_instruction()
        )
        logger.info("WireframeGeneratorAgent initialized")
    
    def _get_instruction(self) -> str:
        return WIREFRAME_INSTRUCTION
    
    async def generate(self, screens: List[str], features: List[str] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate wireframes for screens
        
        Args:
            screens: List of screen names to create wireframes for
            features: Optional list of features to include
            context: Optional context about the product
            
        Returns:
            Wireframes for each screen in ASCII format
        """
        logger.info("Generating wireframes", screens_count=len(screens))
        
        try:
            wireframes = {}
            
            for screen in screens:
                # Use agent to identify elements
                features_str = ', '.join(features) if features else 'All relevant features for this screen'
                product_context = str(context.get('original_idea', context.get('feature_request', 'N/A')))[:200] if context else 'N/A'
                prompt = WIREFRAME_PROMPT_TEMPLATE.format(
                    screen=screen,
                    features=features_str,
                    product_context=product_context
                )
                
                agent_response = await call_agent(self.agent, prompt)
                
                # Extract elements from agent response
                # Then use code execution to generate ASCII wireframe
                elements = self._extract_elements(str(agent_response))
                
                # Generate ASCII wireframe
                wireframe = await code_execution.generate_wireframe(screen, elements)
                
                wireframes[screen] = {
                    "screen_name": screen,
                    "wireframe": wireframe,
                    "elements": elements,
                    "raw_analysis": str(agent_response)
                }
            
            result = {
                "wireframes": wireframes,
                "total_screens": len(screens)
            }
            
            logger.info("Wireframes generated", screens=len(screens))
            return result
            
        except Exception as e:
            logger.error("Wireframe generation failed", error=str(e))
            return {
                "error": str(e),
                "wireframes": {}
            }
    
    def _extract_elements(self, text: str) -> List[str]:
        """Extract UI elements from agent response"""
        # Simple extraction - in production, use more sophisticated parsing
        elements = []
        common_elements = [
            "Login Button", "Sign Up Button", "Search Bar", "Navigation Menu",
            "User Profile", "Settings", "Home Button", "Back Button",
            "Submit Button", "Cancel Button", "Input Field", "Dropdown",
            "Checkbox", "Radio Button", "Image", "Video Player", "Text Area"
        ]
        
        # Look for common elements in text
        text_lower = text.lower()
        for elem in common_elements:
            if elem.lower() in text_lower:
                elements.append(elem)
        
        # If no elements found, add defaults
        if not elements:
            elements = ["Header", "Content Area", "Footer", "Navigation"]
        
        return elements[:8]  # Limit to 8 elements

