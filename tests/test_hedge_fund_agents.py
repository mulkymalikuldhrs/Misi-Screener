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
from agents.technical_analyst import TechnicalAnalyst

# --- Fixtures ---

@pytest.fixture
def strategy_dict():
    """Provides the strategy content as a dictionary."""
    strategy_content = """
    strategy_name: "TestRSI"
    asset_ticker: "TEST-ASSET"
    parameters:
      indicator: "rsi"
      rsi_period: 14
      oversold_threshold: 30
      overbought_threshold: 70
    risk_management:
      risk_per_trade_percent: 1.0
    """
    return yaml.safe_load(strategy_content)

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

    def get_historical_data(ticker, period, interval=None):
        return connector.current_data

    connector.get_historical_data.side_effect = get_historical_data
    connector.current_data = full_data_oversold
    return connector

@pytest.fixture
def technical_analyst():
    """Provides a real instance of the TechnicalAnalyst."""
    return TechnicalAnalyst()

# --- Test Cases ---

def test_signal_agent_buy_signal(strategy_dict, mock_data_connector, technical_analyst):
    """Test if the SignalAgent correctly generates a BUY signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["oversold"]
    agent = SignalAgent(strategy_dict, mock_data_connector, technical_analyst)
    signal = agent.generate_signal()
    assert signal == "BUY"

def test_signal_agent_sell_signal(strategy_dict, mock_data_connector, technical_analyst):
    """Test if the SignalAgent correctly generates a SELL signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["overbought"]
    agent = SignalAgent(strategy_dict, mock_data_connector, technical_analyst)
    signal = agent.generate_signal()
    assert signal == "SELL"

def test_portfolio_manager_position_sizing(mock_data_connector):
    """Test the position sizing calculation."""
    pm = PortfolioManager(data_connector=mock_data_connector, initial_cash=100000)
    pm._calculate_total_value = MagicMock(return_value=100000)

    position_size = pm.calculate_position_size(
        risk_per_trade_percent=1.0,
        entry_price=100.0,
        stop_loss_price=98.0
    )
    assert position_size == 500.0

def test_portfolio_manager_trade_recording(mock_data_connector):
    """Test that recording a trade correctly updates cash, positions, and value."""
    pm = PortfolioManager(data_connector=mock_data_connector, initial_cash=100000)
    mock_data_connector.current_data = pd.DataFrame({'Close': [110.0]})

    pm.record_trade(ticker="TEST", side="BUY", units=10, price=100, reason="ENTRY")
    state = pm.get_state()
    assert state['cash'] == 99000
    assert "TEST" in state['positions']
    assert state['positions']['TEST']['units'] == 10
    assert state['portfolio_value'] == 100100  # (10 * 110) + 99000

    pm.record_trade(ticker="TEST", side="SELL", units=5, price=110, reason="TAKE_PROFIT")
    mock_data_connector.current_data = pd.DataFrame({'Close': [115.0]})
    state = pm.get_state()
    assert state['cash'] == 99550
    assert state['positions']['TEST']['units'] == 5
    assert state['portfolio_value'] == 100125  # (5 * 115) + 99550

    pm.record_trade(ticker="TEST", side="SELL", units=5, price=115, reason="FINAL_EXIT")
    state = pm.get_state()
    assert state['cash'] == 100125
    assert "TEST" not in state['positions']
    assert state['portfolio_value'] == 100125
