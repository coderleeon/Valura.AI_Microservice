import json
from typing import List, Dict, Any, Optional
from src.models.schemas import Intent, ClassifierOutput, Message, SafetyStatus
from src.services.llm import llm_service
from src.memory.session import session_manager

class IntentClassifier:
    """
    Classifies user intent using a single LLM call.
    Uses conversation memory for context and a simple query cache.
    """
    def __init__(self):
        self._cache: Dict[str, ClassifierOutput] = {}
    
    SYSTEM_PROMPT = """
    You are an intent classifier for a financial AI agent.
    Analyze the user query and conversation history.
    Respond with a strict JSON object:
    {
      "intent": "portfolio_health" | "trade_execution" | "market_analysis" | "general_query",
      "agent": "portfolio_health_agent" | "trade_agent" | "market_agent" | "stub_agent",
      "entities": { ... extracted entities like tickers, amounts ... },
      "safety": { "is_safe": boolean, "reason": string | null }
    }
    """

    async def classify(self, session_id: str, query: str) -> ClassifierOutput:
        normalized_query = query.strip().lower()
        
        # Check Cache
        if normalized_query in self._cache:
            print(f"DEBUG: Cache hit for query: {normalized_query}")
            return self._cache[normalized_query]

        # 1. Retrieve history for follow-up support
        history = session_manager.get_history(session_id)
        
        # 2. Prepare messages for LLM
        messages = [Message(role="system", content=self.SYSTEM_PROMPT)]
        messages.extend(history)
        messages.append(Message(role="user", content=query))
        
        try:
            # 3. Single LLM call
            raw_output = await llm_service.generate_json(messages)
            
            # 4. Map to ClassifierOutput schema
            result = ClassifierOutput(
                intent=Intent(raw_output.get("intent", "unknown")),
                agent=raw_output.get("agent", "stub_agent"),
                entities=raw_output.get("entities", {}),
                safety=SafetyStatus(
                    is_safe=raw_output.get("safety", {}).get("is_safe", True),
                    reason=raw_output.get("safety", {}).get("reason")
                )
            )
            
            # Update Cache
            self._cache[normalized_query] = result
            return result
        except Exception as e:
            # Fallback if LLM fails
            return ClassifierOutput(
                intent=Intent.UNKNOWN,
                agent="stub_agent",
                entities={},
                safety=SafetyStatus(is_safe=True)
            )

# Singleton instance
classifier = IntentClassifier()
