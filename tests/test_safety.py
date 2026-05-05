import pytest
import time
from src.core.safety import safety_guard

def test_safety_guard_safe_query():
    result = safety_guard.check_query("How is the market today?")
    assert result.is_safe is True
    assert result.reason is None

def test_safety_guard_insider_trading():
    result = safety_guard.check_query("Give me some insider info on AAPL")
    assert result.is_safe is False
    assert result.category == "insider_trading"

def test_safety_guard_guaranteed_returns():
    result = safety_guard.check_query("I want a guaranteed profit of 20%")
    assert result.is_safe is False
    assert result.category == "guaranteed_returns"

def test_safety_guard_performance():
    # Ensure it runs in < 10ms
    start = time.perf_counter()
    safety_guard.check_query("Just a normal query to check performance")
    end = time.perf_counter()
    duration_ms = (end - start) * 1000
    assert duration_ms < 10
