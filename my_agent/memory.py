"""
Memory Management for MAPIS
Uses InMemorySessionService to maintain conversation context
"""
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger(__name__)


class InMemorySessionService:
    """In-memory session service for maintaining conversation context"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        logger.info("InMemorySessionService initialized")
    
    def create_session(self, session_id: str) -> Dict[str, Any]:
        """Create a new session"""
        self.sessions[session_id] = {
            "context": {},
            "history": [],
            "preferences": {},
            "previous_ideas": [],
            "previous_features": []
        }
        logger.info(f"Created session: {session_id}")
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get existing session"""
        return self.sessions.get(session_id)
    
    def update_context(self, session_id: str, key: str, value: Any):
        """Update context in session"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id]["context"][key] = value
        logger.debug(f"Updated context for {session_id}: {key}")
    
    def get_context(self, session_id: str, key: str, default: Any = None) -> Any:
        """Get context value from session"""
        session = self.get_session(session_id)
        if session:
            return session["context"].get(key, default)
        return default
    
    def add_to_history(self, session_id: str, agent_name: str, input_data: Any, output_data: Any):
        """Add interaction to history"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id]["history"].append({
            "agent": agent_name,
            "input": input_data,
            "output": output_data
        })
        logger.debug(f"Added to history for {session_id}: {agent_name}")
    
    def get_history(self, session_id: str) -> list:
        """Get conversation history"""
        session = self.get_session(session_id)
        if session:
            return session["history"]
        return []
    
    def store_preference(self, session_id: str, key: str, value: Any):
        """Store user preference"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id]["preferences"][key] = value
        logger.debug(f"Stored preference for {session_id}: {key}")
    
    def get_preference(self, session_id: str, key: str, default: Any = None) -> Any:
        """Get user preference"""
        session = self.get_session(session_id)
        if session:
            return session["preferences"].get(key, default)
        return default


# Global session service instance
session_service = InMemorySessionService()

