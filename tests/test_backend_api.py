import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.backend.main import app, APP_REGISTRY
from agents.advanced_orchestrator import AdvancedQueryOrchestrator

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

# --- Mocking Data Connectors ---
@pytest.fixture(autouse=True)
def mock_connectors():
    """
    This fixture automatically mocks all data connector methods for every test.
    """
    # We create new MagicMock objects for each test run to reset call counts
    with patch.dict(APP_REGISTRY, {
        "get_historical_data": MagicMock(return_value="chart_data"),
        "get_news_headlines": MagicMock(return_value="news_data"),
        "get_income_statement": MagicMock(return_value="fa_data"),
    }) as mock_registry:
        yield mock_registry

# --- Advanced Orchestrator Tests ---

def test_advanced_orchestrator_multi_ticker():
    """
    Test that the AdvancedQueryOrchestrator can correctly parse multiple tickers.
    """
    orchestrator = AdvancedQueryOrchestrator()
    query = "show me the latest news for AAPL and MSFT"
    app_name, params = orchestrator.parse_query(query)

    assert app_name == "get_news_headlines"
    assert "tickers" in params
    assert sorted(params["tickers"]) == ["AAPL", "MSFT"]

def test_advanced_orchestrator_no_intent():
    """
    Test that the orchestrator returns None when no intent is found.
    """
    orchestrator = AdvancedQueryOrchestrator()
    query = "what is the color of the sky?"
    app_name, params = orchestrator.parse_query(query)

    assert app_name is None

# --- API Endpoint Tests ---

def test_invoke_app_success(client):
    """
    Test that the /invoke/{app_name} endpoint successfully calls the correct
    mocked backend function.
    """
    response = client.get("/api/v1/invoke/get_news_headlines?ticker=GOOG")

    assert response.status_code == 200
    assert response.json() == "news_data"
    APP_REGISTRY["get_news_headlines"].assert_called_once_with(query="GOOG")

def test_invoke_app_not_found(client):
    """
    Test that invoking a non-existent app returns a 404 error.
    """
    response = client.get("/api/v1/invoke/non_existent_app?ticker=FAIL")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_ai_query_multi_asset_success(client):
    """
    Test the /ai-query endpoint with a multi-asset query.
    """
    query = "get revenue for TSLA and AMZN"
    response = client.post("/api/v1/ai-query", json={"query": query})

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["app_name"] == "get_income_statement"
    assert len(json_response["results"]) == 2

    # Check that the underlying function was called for each ticker
    call_args = APP_REGISTRY["get_income_statement"].call_args_list
    assert len(call_args) == 2
    assert call_args[0].kwargs == {'ticker': 'TSLA'}
    assert call_args[1].kwargs == {'ticker': 'AMZN'}

def test_ai_query_unclear_intent(client):
    """
    Test the /ai-query endpoint with a query the agent cannot parse.
    """
    query = "tell me a joke"
    response = client.post("/api/v1/ai-query", json={"query": query})

    assert response.status_code == 400
    assert "Could not understand the query" in response.json()["detail"]
