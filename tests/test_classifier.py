import pytest
import asyncio
from src.core.classifier import classifier
from src.memory.session import session_manager

@pytest.mark.asyncio
async def test_classifier_portfolio_intent():
    session_id = "test_user_1"
    query = "How is my portfolio health looking?"
    
    result = await classifier.classify(session_id, query)
    
    assert result.intent == "portfolio_health"
    assert result.agent == "portfolio_health_agent"
    assert result.safety.is_safe is True

@pytest.mark.asyncio
async def test_classifier_history_support():
    session_id = "test_user_2"
    
    # Pre-populate history
    session_manager.add_message(session_id, "user", "What is AAPL price?")
    session_manager.add_message(session_id, "assistant", "AAPL is $180.")
    
    # Follow-up query
    query = "What about its market health?"
    
    result = await classifier.classify(session_id, query)
    
    # In MockLLM, 'market' triggers market_analysis
    assert result.intent == "market_analysis"
    assert result.agent == "market_agent"
