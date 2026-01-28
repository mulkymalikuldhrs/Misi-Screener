import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import os
import sys

# Ensure the app directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.backend.main import app, state_manager

@pytest.fixture(autouse=True)
def reset_state_manager():
    """Fixture to reset the singleton state manager before each test."""
    state_manager.master_agent = None
    state_manager.portfolio_manager = None
    state_manager.agent_task = None
    yield

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

# --- API Endpoint Tests ---

def test_list_strategies_success(client):
    """
    Test that the /strategies endpoint correctly finds and parses strategy files.
    """
    # Mock the os.listdir and yaml.safe_load calls to avoid file system dependency
    mock_files = ["strategy_a.yml", "strategy_b.yml", "not_a_strategy.txt"]
    mock_strategy_a = {
        "strategy_name": "Strategy A",
        "strategy_description": "Description A"
    }
    mock_strategy_b = {
        "strategy_name": "Strategy B",
        "strategy_description": "Description B"
    }

    with patch("os.listdir", MagicMock(return_value=mock_files)):
        with patch("builtins.open", MagicMock()):
            with patch("yaml.safe_load", side_effect=[mock_strategy_a, mock_strategy_b]) as mock_yaml:
                response = client.get("/api/v1/strategies")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["filename"] == "strategy_a.yml"
    assert response.json()[0]["strategy_name"] == "Strategy A"
    assert response.json()[1]["filename"] == "strategy_b.yml"
    assert response.json()[1]["strategy_name"] == "Strategy B"

@patch("dashboard.backend.main.HedgeFundMasterAgent")
@patch("os.path.exists", return_value=True)
def test_start_agent_success(mock_path_exists, MockMasterAgent, client):
    """
    Test the successful start of a trading agent.
    """
    # Mock the async start method
    mock_agent_instance = MockMasterAgent.return_value
    mock_agent_instance.start = AsyncMock()

    # Mock the strategy file reading to prevent FileNotFoundError
    mock_strategy = {"strategy_name": "Test Strategy"}
    with patch("builtins.open", MagicMock()):
        with patch("yaml.safe_load", return_value=mock_strategy):
            response = client.post("/api/v1/agent/start", json={"strategy_filename": "test_strategy.yml"})

    assert response.status_code == 200
    assert response.json()["status"] == "Hedge Fund Master Agent started successfully."
    assert state_manager.is_agent_running() is True
    assert state_manager.agent_task is not None

def test_start_agent_when_already_running(client):
    """
    Test that starting an agent fails if one is already running.
    """
    # Simulate an agent already running
    state_manager.master_agent = MagicMock()
    state_manager.master_agent.is_running = True

    response = client.post("/api/v1/agent/start", json={"strategy_filename": "test_strategy.yml"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Agent is already running."

def test_start_agent_strategy_not_found(client):
    """
    Test that starting an agent fails if the strategy file doesn't exist.
    """
    with patch("os.path.exists", return_value=False):
        response = client.post("/api/v1/agent/start", json={"strategy_filename": "non_existent.yml"})

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_stop_agent_success(client):
    """
    Test successfully stopping a running agent.
    """
    mock_agent = MagicMock()
    mock_agent.is_running = True
    state_manager.master_agent = mock_agent
    state_manager.agent_task = MagicMock()

    response = client.post("/api/v1/agent/stop")

    assert response.status_code == 200
    mock_agent.stop.assert_called_once()
    # Check that the task was cancelled, if it existed
    if state_manager.agent_task:
        state_manager.agent_task.cancel.assert_called_once()
    assert state_manager.master_agent is None

def test_stop_agent_not_running(client):
    """
    Test that stopping fails if no agent is running.
    """
    response = client.post("/api/v1/agent/stop")
    assert response.status_code == 400
    assert response.json()["detail"] == "Agent is not currently running."

def test_get_agent_status(client):
    """
    Test the agent status endpoint.
    """
    response = client.get("/api/v1/agent/status")
    assert response.status_code == 200
    assert response.json() == {"is_running": False}

    # Simulate running agent
    state_manager.master_agent = MagicMock()
    state_manager.master_agent.is_running = True
    response = client.get("/api/v1/agent/status")
    assert response.status_code == 200
    assert response.json() == {"is_running": True}

def test_get_portfolio_state_success(client):
    """
    Test retrieving the portfolio state.
    """
    mock_portfolio = MagicMock()
    mock_portfolio.get_state.return_value = {"cash": 50000, "value": 55000}
    state_manager.portfolio_manager = mock_portfolio

    response = client.get("/api/v1/portfolio/state")
    assert response.status_code == 200
    assert response.json() == {"cash": 50000, "value": 55000}

def test_get_portfolio_state_not_initialized(client):
    """
    Test retrieving portfolio state when the agent hasn't been started.
    """
    response = client.get("/api/v1/portfolio/state")
    assert response.status_code == 200
    assert "Portfolio not initialized" in response.json()["status"]
