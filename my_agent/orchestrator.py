"""
Final Output Aggregator (Orchestrator)
Orchestrates agent workflows and aggregates outputs
"""
from typing import Dict, Any, List
import structlog
import asyncio
from .memory import session_service
from .agents.intent_classification_agent import IntentClassificationAgent
from .agents.domain_understanding_agent import DomainUnderstandingAgent
from .agents.idea_breakdown_agent import IdeaBreakdownAgent
from .agents.feature_design_agent import FeatureDesignAgent
from .agents.competitor_analysis_agent import CompetitorAnalysisAgent
from .agents.architecture_suggestion_agent import ArchitectureSuggestionAgent
from .agents.market_size_agent import MarketSizeAgent
from .agents.wireframe_generator_agent import WireframeGeneratorAgent
from .agents.concept_paper_writer_agent import ConceptPaperWriterAgent
from .agents.pitch_creator_agent import PitchCreatorAgent
from .utils.logger import log_agent_execution

logger = structlog.get_logger(__name__)


class MAPISOrchestrator:
    """Orchestrates the Multi-Agent Product Innovation System"""
    
    def __init__(self):
        # Initialize all agents
        self.intent_agent = IntentClassificationAgent()
        self.domain_agent = DomainUnderstandingAgent()
        self.idea_breakdown_agent = IdeaBreakdownAgent()
        self.feature_design_agent = FeatureDesignAgent()
        self.competitor_agent = CompetitorAnalysisAgent()
        self.architecture_agent = ArchitectureSuggestionAgent()
        self.market_size_agent = MarketSizeAgent()
        self.wireframe_agent = WireframeGeneratorAgent()
        self.concept_paper_agent = ConceptPaperWriterAgent()
        self.pitch_agent = PitchCreatorAgent()
        
        logger.info("MAPISOrchestrator initialized with all agents")
    
    @log_agent_execution("orchestrator")
    async def process(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Main orchestration method - processes user input through agent pipeline
        
        Args:
            user_input: User's request
            session_id: Session ID for memory management
            
        Returns:
            Complete output with all agent results
        """
        logger.info("Starting MAPIS orchestration", session_id=session_id, input_length=len(user_input))
        
        # Ensure session exists
        session_service.create_session(session_id)
        session_service.update_context(session_id, "user_input", user_input)
        
        try:
            # Step 1: Classify intent
            intent_result = await self.intent_agent.classify(user_input)
            session_service.add_to_history(session_id, "intent_classification", user_input, intent_result)
            session_service.update_context(session_id, "intent", intent_result)
            
            intent = intent_result.get("intent", "new_app_idea")
            domain = intent_result.get("domain")
            keywords = intent_result.get("keywords", [])
            
            logger.info("Intent classified", intent=intent, domain=domain)
            
            # Route based on intent
            if intent == "new_app_idea":
                return await self._process_new_app_idea(user_input, domain, keywords, session_id)
            elif intent == "feature_extension":
                return await self._process_feature_extension(user_input, domain, keywords, session_id)
            else:
                # Default to new app idea
                return await self._process_new_app_idea(user_input, domain, keywords, session_id)
                
        except Exception as e:
            logger.error("Orchestration failed", error=str(e), session_id=session_id)
            return {
                "error": str(e),
                "session_id": session_id,
                "user_input": user_input
            }
    
    async def _process_new_app_idea(self, user_input: str, domain: str, keywords: List[str], session_id: str) -> Dict[str, Any]:
        """Process new app idea workflow"""
        logger.info("Processing new app idea workflow", domain=domain)
        
        results = {
            "intent": "new_app_idea",
            "user_input": user_input,
            "domain": domain,
            "keywords": keywords
        }
        
        try:
            # Step 2: Domain Understanding (can run in parallel with idea breakdown prep)
            domain_task = self.domain_agent.analyze(domain or "General", keywords)
            
            # Step 3: Idea Breakdown (can start with basic context)
            idea_task = self.idea_breakdown_agent.breakdown(user_input)
            
            # Wait for both
            domain_result, idea_result = await asyncio.gather(domain_task, idea_task)
            
            results["domain_analysis"] = domain_result
            results["idea_breakdown"] = idea_result
            session_service.add_to_history(session_id, "domain_understanding", domain, domain_result)
            session_service.add_to_history(session_id, "idea_breakdown", user_input, idea_result)
            
            # Step 4: Competitor Analysis (parallel with market size)
            product_type = idea_result.get("value_proposition", "product")[:50]
            competitor_task = self.competitor_agent.analyze(
                domain or "General",
                product_type,
                idea_result
            )
            
            market_task = self.market_size_agent.calculate(
                domain or "General",
                product_type,
                "global",
                idea_result
            )
            
            competitor_result, market_result = await asyncio.gather(competitor_task, market_task)
            
            results["competitor_analysis"] = competitor_result
            results["market_size"] = market_result
            session_service.add_to_history(session_id, "competitor_analysis", domain, competitor_result)
            session_service.add_to_history(session_id, "market_size", domain, market_result)
            
            # Step 5: Architecture Suggestion
            features = idea_result.get("proposed_features", [])
            architecture_result = await self.architecture_agent.suggest(idea_result, features)
            results["architecture"] = architecture_result
            session_service.add_to_history(session_id, "architecture", idea_result, architecture_result)
            
            # Step 6: Wireframe Generation
            screens = ["Login", "Home", "Main Feature", "Settings"]  # Default screens
            wireframe_result = await self.wireframe_agent.generate(screens, features, idea_result)
            results["wireframes"] = wireframe_result
            session_service.add_to_history(session_id, "wireframes", screens, wireframe_result)
            
            # Step 7: Pitch Creation
            pitch_result = await self.pitch_agent.create(idea_result, market_result, competitor_result)
            results["pitch"] = pitch_result
            session_service.add_to_history(session_id, "pitch", idea_result, pitch_result)
            
            # Final aggregation
            results["status"] = "success"
            results["summary"] = self._create_summary(results)
            
            logger.info("New app idea workflow completed", domain=domain)
            return results
            
        except Exception as e:
            logger.error("New app idea workflow failed", error=str(e))
            results["error"] = str(e)
            results["status"] = "error"
            return results
    
    async def _process_feature_extension(self, user_input: str, domain: str, keywords: List[str], session_id: str) -> Dict[str, Any]:
        """Process feature extension workflow"""
        logger.info("Processing feature extension workflow", domain=domain)
        
        results = {
            "intent": "feature_extension",
            "user_input": user_input,
            "domain": domain,
            "keywords": keywords
        }
        
        try:
            # Extract app name and feature from input
            # Simple extraction - can be enhanced
            app_name = self._extract_app_name(user_input)
            feature_request = user_input
            
            # Step 2: Feature Design
            feature_result = await self.feature_design_agent.design(app_name, feature_request)
            results["feature_design"] = feature_result
            session_service.add_to_history(session_id, "feature_design", user_input, feature_result)
            
            # Step 3: Concept Paper (can run in parallel with competitor analysis)
            concept_task = self.concept_paper_agent.write(feature_result, app_name)
            
            competitor_task = self.competitor_agent.analyze(
                domain or "General",
                f"{app_name} feature",
                feature_result
            )
            
            concept_result, competitor_result = await asyncio.gather(concept_task, competitor_task)
            
            results["concept_paper"] = concept_result
            results["competitor_analysis"] = competitor_result
            session_service.add_to_history(session_id, "concept_paper", feature_result, concept_result)
            session_service.add_to_history(session_id, "competitor_analysis", domain, competitor_result)
            
            # Step 4: Wireframe Generation
            screens = feature_result.get("user_journey", ["Feature Screen"])
            if not screens or isinstance(screens, str):
                screens = ["Feature Screen", "Settings"]
            
            features = feature_result.get("user_stories", [])
            wireframe_result = await self.wireframe_agent.generate(screens, features, feature_result)
            results["wireframes"] = wireframe_result
            session_service.add_to_history(session_id, "wireframes", screens, wireframe_result)
            
            # Step 5: Architecture (for feature integration)
            architecture_result = await self.architecture_agent.suggest(feature_result, features)
            results["architecture"] = architecture_result
            session_service.add_to_history(session_id, "architecture", feature_result, architecture_result)
            
            # Final aggregation
            results["status"] = "success"
            results["summary"] = self._create_summary(results)
            
            logger.info("Feature extension workflow completed", app=app_name)
            return results
            
        except Exception as e:
            logger.error("Feature extension workflow failed", error=str(e))
            results["error"] = str(e)
            results["status"] = "error"
            return results
    
    def _extract_app_name(self, user_input: str) -> str:
        """Extract app name from user input"""
        # Simple extraction - look for common patterns
        # "Add X to Y" or "Enhance Y with X"
        words = user_input.split()
        common_apps = ["Swiggy", "Instagram", "Facebook", "Twitter", "LinkedIn", "Uber", "Zomato"]
        
        for app in common_apps:
            if app.lower() in user_input.lower():
                return app
        
        # Default
        return "Application"
    
    def _create_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of all results"""
        return {
            "intent": results.get("intent"),
            "domain": results.get("domain"),
            "status": results.get("status"),
            "agents_executed": len([k for k in results.keys() if k not in ["intent", "user_input", "domain", "keywords", "status", "summary", "error"]]),
            "has_wireframes": "wireframes" in results,
            "has_architecture": "architecture" in results,
            "has_market_data": "market_size" in results
        }

