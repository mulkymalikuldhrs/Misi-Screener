import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Make sure the app can be imported
# This requires the root of the project to be in the PYTHONPATH
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.backend.main import app, APP_REGISTRY

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

# --- Mocking Data Connectors ---
# We mock the actual data-fetching methods to isolate the API layer for testing.
@pytest_asyncio.fixture(autouse=True)
def mock_connectors():
    """
    This fixture automatically mocks all data connector methods for every test.
    It prevents real API calls from being made during tests.
    """
    with patch.dict(APP_REGISTRY, {
        "get_historical_data": MagicMock(return_value=[{"date": "2023-01-01", "close": 150.0}]),
        "get_news_headlines": MagicMock(return_value=[{"title": "Test News"}]),
        "get_income_statement": MagicMock(return_value={"report": "Test Report"}),
    }) as mock_registry:
        yield mock_registry

# --- Test Cases ---

def test_invoke_app_success(client, mock_connectors):
    """
    Test that the /invoke/{app_name} endpoint successfully calls the correct
    mocked backend function.
    """
    app_name = "get_news_headlines"
    response = client.get(f"/api/v1/invoke/{app_name}?ticker=AAPL")

    assert response.status_code == 200
    assert response.json() == [{"title": "Test News"}]
    # Check that the correct mock function was called with the right parameter
    APP_REGISTRY[app_name].assert_called_once_with(query="AAPL")

def test_invoke_app_not_found(client):
    """
    Test that invoking a non-existent app returns a 404 error.
    """
    response = client.get("/api/v1/invoke/non_existent_app?ticker=FAIL")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_ai_query_success(client, mock_connectors):
    """
    Test the /ai-query endpoint with a query that should be successfully parsed.
    """
    query = "show me the latest news for MSFT"
    response = client.post("/api/v1/ai-query", json={"query": query})

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["app_name"] == "get_news_headlines"
    assert json_response["data"] == [{"title": "Test News"}]
    # Check that the mock function was called with the ticker parsed by the orchestrator
    APP_REGISTRY["get_news_headlines"].assert_called_with(query="MSFT")

def test_ai_query_unclear_intent(client):
    """
    Test the /ai-query endpoint with a query that the orchestrator cannot parse.
    """
    query = "what is the color of the sky?"
    response = client.post("/api/v1/ai-query", json={"query": query})

    assert response.status_code == 400
    assert "Could not understand the query" in response.json()["detail"]
