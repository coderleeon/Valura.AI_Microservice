import pytest
import json
from src.core.router import router
from src.models.schemas import ClassifierOutput, Intent, SafetyStatus, PortfolioData

def test_router_to_portfolio_agent():
    output = ClassifierOutput(
        intent=Intent.PORTFOLIO_HEALTH,
        agent="portfolio_health_agent",
        safety=SafetyStatus(is_safe=True)
    )
    portfolio = PortfolioData(items=[])
    response = router.route(output, portfolio)
    
    content = json.loads(response.content)
    assert content["status"] == "empty_portfolio"

def test_router_to_stub_agent():
    output = ClassifierOutput(
        intent=Intent.MARKET_ANALYSIS,
        agent="market_agent",
        safety=SafetyStatus(is_safe=True)
    )
    portfolio = PortfolioData(items=[])
    response = router.route(output, portfolio)
    
    assert "under development" in response.content

def test_router_crash_prevention():
    # Pass None to force an exception
    response = router.route(None, None)
    assert "unexpected error" in response.content
