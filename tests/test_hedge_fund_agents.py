import pytest
import pandas as pd
import yaml
from unittest.mock import MagicMock

# Ensure modules can be imported
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.signal_agent import SignalAgent
from agents.portfolio_manager import PortfolioManager
from agents.technical_analyst import TechnicalAnalystAgent
from agents.strategy_manager import StrategyManager
from agents.models import db, PortfolioState, Position, Trade

# --- Fixtures ---

@pytest.fixture(autouse=True)
def setup_test_db():
    """Sets up an in-memory database for each test."""
    db.init(':memory:')
    db.connect(reuse_if_open=True)
    db.create_tables([PortfolioState, Position, Trade])
    yield
    db.close()

@pytest.fixture
def mock_strategy_file(tmp_path):
    """Creates a temporary YAML strategy file for testing."""
    strategy_content = """
    strategy_name: "TestRSI"
    asset_ticker: "TEST-ASSET"
    timeframe: "1h"
    parameters:
      rsi_period: 14
      oversold_threshold: 30
      overbought_threshold: 70
    risk_management:
      risk_per_trade_percent: 1.0
      stop_loss_method: "fixed_percent"
      stop_loss_percent: 2.0
    """
    p = tmp_path / "strategy.yml"
    p.write_text(strategy_content)
    return str(p)

@pytest.fixture
def strategy_manager(mock_strategy_file):
    return StrategyManager(mock_strategy_file)

@pytest.fixture
def mock_data_connector():
    """Mocks the data connector to return predictable data."""
    connector = MagicMock()

    # Create a DataFrame with a clear RSI signal
    price_data_oversold = pd.DataFrame({
        'Close': [50, 48, 46, 45, 43, 40, 38, 35, 33, 30, 28, 25, 22, 20, 18],
        'High': [51, 49, 47, 46, 44, 41, 39, 36, 34, 31, 29, 26, 23, 21, 19],
        'Low': [49, 47, 45, 44, 42, 39, 37, 34, 32, 29, 27, 24, 21, 19, 17]
    })
    full_data_oversold = pd.concat([pd.DataFrame({'Close': [50]*20, 'High': [51]*20, 'Low': [49]*20}), price_data_oversold], ignore_index=True)

    price_data_overbought = pd.DataFrame({
        'Close': [50, 52, 54, 55, 57, 60, 62, 65, 67, 70, 72, 75, 78, 80, 82],
        'High': [51, 53, 55, 56, 58, 61, 63, 66, 68, 71, 73, 76, 79, 81, 83],
        'Low': [49, 51, 53, 54, 56, 59, 61, 64, 66, 69, 71, 74, 77, 79, 81]
    })
    full_data_overbought = pd.concat([pd.DataFrame({'Close': [50]*20, 'High': [51]*20, 'Low': [49]*20}), price_data_overbought], ignore_index=True)

    connector.mock_data = {
        "oversold": full_data_oversold,
        "overbought": full_data_overbought
    }

    def get_historical_data(ticker, period):
        return connector.current_data

    connector.get_historical_data.side_effect = get_historical_data
    connector.current_data = full_data_oversold # Default
    return connector

@pytest.fixture
def technical_analyst():
    return TechnicalAnalystAgent()

# --- Test Cases ---

def test_signal_agent_buy_signal(strategy_manager, mock_data_connector, technical_analyst):
    """Test if the SignalAgent correctly generates a BUY signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["oversold"]
    agent = SignalAgent(strategy_manager, mock_data_connector, technical_analyst)
    signal = agent.generate_signal()
    assert signal == "BUY"

def test_signal_agent_sell_signal(strategy_manager, mock_data_connector, technical_analyst):
    """Test if the SignalAgent correctly generates a SELL signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["overbought"]
    agent = SignalAgent(strategy_manager, mock_data_connector, technical_analyst)
    signal = agent.generate_signal()
    assert signal == "SELL"

def test_portfolio_manager_position_sizing(mock_data_connector):
    """Test the position sizing calculation."""
    pm = PortfolioManager(data_connector=mock_data_connector, initial_cash=100000)
    pm.get_current_price = MagicMock(return_value=100.0)

    position_size = pm.calculate_position_size(
        risk_per_trade_percent=1.0,
        entry_price=100.0,
        stop_loss_price=98.0
    )
    assert position_size == 500.0

def test_portfolio_manager_trade_recording(mock_data_connector):
    """Test that recording a trade correctly updates cash and positions."""
    pm = PortfolioManager(data_connector=mock_data_connector, initial_cash=100000)
    pm.get_current_price = MagicMock(return_value=110.0)

    # Buy 10 units of TEST at $100
    pm.record_trade(ticker="TEST", side="BUY", units=10, price=100, reason="ENTRY")

    state = pm.get_state()
    assert state['cash'] == 99000 # 100000 - (10 * 100)
    assert "TEST" in state['positions']
    assert state['positions']['TEST']['units'] == 10

    # Value: 99000 (cash) + 10 * 110 (market price) = 100100
    assert state['portfolio_value'] == 100100

    # Sell 5 units of TEST at $110
    pm.record_trade(ticker="TEST", side="SELL", units=5, price=110, reason="TAKE_PROFIT")

    state = pm.get_state()
    assert state['cash'] == 99550 # 99000 + (5 * 110)
    assert state['positions']['TEST']['units'] == 5

    # Sell remaining 5 units
    pm.record_trade(ticker="TEST", side="SELL", units=5, price=115, reason="FINAL_EXIT")

    state = pm.get_state()
    assert state['cash'] == 100125 # 99550 + (5 * 115)
    assert "TEST" not in state['positions']
