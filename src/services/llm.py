import json
import abc
from typing import List, Dict, Any, Optional
from src.models.schemas import Message

class BaseLLM(abc.ABC):
    @abc.abstractmethod
    async def generate_json(self, messages: List[Message], schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

class MockLLM(BaseLLM):
    """
    Mock LLM implementation for deterministic testing.
    No external network calls.
    """
    def __init__(self):
        self.default_responses = {
            "portfolio_health": {
                "intent": "portfolio_health",
                "agent": "portfolio_health_agent",
                "entities": {"portfolio_context": "current_user"},
                "safety": {"is_safe": True}
            },
            "market_analysis": {
                "intent": "market_analysis",
                "agent": "market_agent",
                "entities": {"ticker": "AAPL"},
                "safety": {"is_safe": True}
            },
            "trade_execution": {
                "intent": "trade_execution",
                "agent": "trade_agent",
                "entities": {"symbol": "AAPL", "quantity": 10},
                "safety": {"is_safe": True}
            },
            "general_query": {
                "intent": "general_query",
                "agent": "stub_agent",
                "entities": {},
                "safety": {"is_safe": True}
            }
        }

    async def generate_json(self, messages: List[Message], schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        last_message = messages[-1].content.lower()
        
        # Simple logic to simulate intent detection
        if "buy" in last_message or "sell" in last_message or "trade" in last_message:
            return self.default_responses["trade_execution"]
        elif "price" in last_message or "market" in last_message:
            return self.default_responses["market_analysis"]
        elif "portfolio" in last_message or "health" in last_message or "concentration" in last_message:
            return self.default_responses["portfolio_health"]
        
        return self.default_responses["general_query"]

# In production, this would be replaced by an actual OpenAI/Gemini provider
llm_service = MockLLM()
