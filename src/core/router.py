from typing import Dict, Any
from src.models.schemas import ClassifierOutput, AgentResponse, PortfolioData
from src.agents.portfolio_health import portfolio_health_agent
from src.agents.stub_agent import stub_agent

class Router:
    """
    Routes the request to the appropriate agent.
    Ensures the system never crashes by using stub fallbacks.
    """
    
    def route(self, classifier_output: ClassifierOutput, portfolio_data: PortfolioData) -> AgentResponse:
        try:
            agent_name = classifier_output.agent
            
            if agent_name == "portfolio_health_agent":
                return portfolio_health_agent.run(portfolio_data)
            
            # Fallback for all other agents (market, trade, etc.)
            return stub_agent.run(classifier_output.intent)
            
        except Exception as e:
            # Emergency fallback to ensure no crashes
            return AgentResponse(
                content="I encountered an unexpected error while routing your request. Please try again.",
                metadata={"error": str(e)}
            )

# Singleton
router = Router()
