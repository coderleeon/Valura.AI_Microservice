from typing import Dict, List, Optional
from src.models.schemas import ChatSession, Message

class SessionManager:
    """
    In-memory session management for basic conversation memory.
    """
    def __init__(self):
        self._sessions: Dict[str, ChatSession] = {}

    def get_or_create_session(self, session_id: str) -> ChatSession:
        if session_id not in self._sessions:
            self._sessions[session_id] = ChatSession(session_id=session_id)
        return self._sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        session = self.get_or_create_session(session_id)
        session.messages.append(Message(role=role, content=content))
        
    def get_history(self, session_id: str) -> List[Message]:
        session = self.get_or_create_session(session_id)
        return session.messages

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]

# Singleton instance
session_manager = SessionManager()
