import json
import asyncio
from typing import AsyncGenerator, Any, Dict, Optional
from src.models.schemas import PortfolioData, ClassifierOutput
from src.core.safety import safety_guard
from src.core.classifier import classifier
from src.core.router import router
from src.memory.session import session_manager

class StreamingService:
    """
    Handles standardized SSE streaming with rich metadata.
    Events: stage_update | final_response | error
    """

    def _format_event(self, 
                     stage: str, 
                     status: str, 
                     agent: str = "none", 
                     intent: str = "none", 
                     data: Any = None) -> Dict[str, Any]:
        return {
            "stage": stage,
            "status": status,
            "agent": agent,
            "intent": intent,
            "data": data
        }

    async def stream_orchestration(self, session_id: str, query: str, portfolio_data: PortfolioData) -> AsyncGenerator[Dict[str, Any], None]:
        current_agent = "none"
        current_intent = "none"
        
        try:
            # 1. Safety Guard
            yield {
                "event": "stage_update", 
                "data": json.dumps(self._format_event("safety", "success", data="Analyzing safety..."))
            }
            safety_result = safety_guard.check_query(query)
            
            if not safety_result.is_safe:
                yield {
                    "event": "error", 
                    "data": json.dumps(self._format_event("safety", "failed", data=f"Safety violation: {safety_result.reason}"))
                }
                return

            # 2. Classification
            yield {
                "event": "stage_update", 
                "data": json.dumps(self._format_event("classification", "success", data="Detecting intent..."))
            }
            classification = await classifier.classify(session_id, query)
            current_agent = classification.agent
            current_intent = classification.intent
            
            if not classification.safety.is_safe:
                yield {
                    "event": "error", 
                    "data": json.dumps(self._format_event("classification", "failed", agent=current_agent, intent=current_intent, data=classification.safety.reason))
                }
                return

            # 3. Routing
            yield {
                "event": "stage_update", 
                "data": json.dumps(self._format_event("routing", "success", agent=current_agent, intent=current_intent, data=f"Executing {current_agent}..."))
            }
            
            # 4. Agent Execution
            agent_response = router.route(classification, portfolio_data)
            
            # Update History
            session_manager.add_message(session_id, "user", query)
            session_manager.add_message(session_id, "assistant", agent_response.content)
            
            # 5. Final Response
            yield {
                "event": "final_response", 
                "data": json.dumps(self._format_event(
                    "response", 
                    "success", 
                    agent=current_agent, 
                    intent=current_intent, 
                    data=json.loads(agent_response.content) if current_agent == "portfolio_health_agent" else agent_response.content
                ))
            }

        except Exception as e:
            yield {
                "event": "error", 
                "data": json.dumps(self._format_event(
                    "response", 
                    "failed", 
                    agent=current_agent, 
                    intent=current_intent, 
                    data=str(e)
                ))
            }

# Singleton
streaming_service = StreamingService()
