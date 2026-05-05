import json
from src.agents.portfolio_health import portfolio_health_agent
from src.agents.stub_agent import stub_agent
from src.models.schemas import PortfolioData, PortfolioItem

def test_portfolio_health_normal():
    data = PortfolioData(items=[
        PortfolioItem(symbol="AAPL", quantity=10, price=150.0, sector="Technology"),
        PortfolioItem(symbol="VTI", quantity=5, price=200.0, sector="Index")
    ])
    response = portfolio_health_agent.run(data)
    
    content = json.loads(response.content)
    assert "concentration_risk" in content
    assert content["performance"]["total_return_pct"] == 0.12
    assert response.metadata["total_value"] == 2500.0

def test_portfolio_health_empty():
    data = PortfolioData(items=[])
    response = portfolio_health_agent.run(data)
    
    content = json.loads(response.content)
    assert "build your financial future" in content["message"].lower()
    assert len(content["guidance"]) == 3

def test_portfolio_health_concentration():
    data = PortfolioData(items=[
        PortfolioItem(symbol="AAPL", quantity=10, price=100.0, sector="Technology")
    ])
    response = portfolio_health_agent.run(data)
    content = json.loads(response.content)
    assert content["concentration_risk"]["flag"] == "high"

def test_stub_agent():
    response = stub_agent.run("market_analysis")
    assert "under development" in response.content
