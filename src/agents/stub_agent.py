from src.models.schemas import AgentResponse

class StubAgent:
    """
    Fallback agent for unimplemented intents.
    Ensures the system never crashes.
    """
    def run(self, intent: str) -> AgentResponse:
        return AgentResponse(
            content=f"I've identified your intent as '{intent}', but this specific agent is still under development. Please check back soon!",
            metadata={"intent_captured": intent, "status": "stub_response"}
        )

# Singleton
stub_agent = StubAgent()
