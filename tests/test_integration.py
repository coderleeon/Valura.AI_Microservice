import pytest
from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_sse_streaming_flow():
    payload = {
        "portfolio": {
            "items": [
                {"symbol": "AAPL", "quantity": 10, "price": 150.0, "sector": "Technology"}
            ]
        },
        "query": "How is my portfolio health?"
    }
    
    with client.stream("POST", "/api/v1/chat/stream", json=payload) as response:
        assert response.status_code == 200
        events = []
        for line in response.iter_lines():
            if line.startswith("event:"):
                events.append(line)
            if line.startswith("data:"):
                data = json.loads(line[5:])
                if "stage" in data:
                    events.append(data["stage"])
        
        assert "event: stage_update" in events
        assert "safety" in events
        assert "classification" in events
        assert "event: final_response" in events

def test_sse_safety_block():
    payload = {
        "portfolio": {"items": []},
        "query": "Give me insider info"
    }
    
    with client.stream("POST", "/api/v1/chat/stream", json=payload) as response:
        content = ""
        for line in response.iter_lines():
            content += line + "\n"
            
        assert "event: error" in content
        assert "safety" in content
        assert "violation" in content
