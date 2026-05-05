from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Intent(str, Enum):
    PORTFOLIO_HEALTH = "portfolio_health"
    TRADE_EXECUTION = "trade_execution"
    MARKET_ANALYSIS = "market_analysis"
    GENERAL_QUERY = "general_query"
    UNKNOWN = "unknown"

class SafetyStatus(BaseModel):
    is_safe: bool
    reason: Optional[str] = None
    category: Optional[str] = None

class Message(BaseModel):
    role: str # 'user' or 'assistant'
    content: str

class ChatSession(BaseModel):
    session_id: str
    messages: List[Message] = []
    metadata: Dict[str, Any] = {}

class PortfolioItem(BaseModel):
    symbol: str
    quantity: float
    price: float
    sector: str

class PortfolioData(BaseModel):
    items: List[PortfolioItem] = []

class ClassifierOutput(BaseModel):
    intent: Intent
    agent: str
    entities: Dict[str, Any] = {}
    safety: SafetyStatus

class AgentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class StreamEvent(BaseModel):
    event: str
    data: Any

class ChatRequest(BaseModel):
    query: str
    portfolio: PortfolioData
