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

# --- Fixtures ---

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
    """
    p = tmp_path / "strategy.yml"
    p.write_text(strategy_content)
    return str(p)

@pytest.fixture
def mock_data_connector():
    """Mocks the data connector to return predictable data."""
    connector = MagicMock()

    # Create a DataFrame with a clear RSI signal
    price_data_oversold = pd.DataFrame({
        'Close': [50, 48, 46, 45, 43, 40, 38, 35, 33, 30, 28, 25, 22, 20, 18]
    })
    # Add more data to make rolling window happy
    full_data_oversold = pd.concat([pd.DataFrame({'Close': [50]*20}), price_data_oversold], ignore_index=True)

    price_data_overbought = pd.DataFrame({
        'Close': [50, 52, 54, 55, 57, 60, 62, 65, 67, 70, 72, 75, 78, 80, 82]
    })
    full_data_overbought = pd.concat([pd.DataFrame({'Close': [50]*20}), price_data_overbought], ignore_index=True)

    # A dictionary to hold different mock datasets
    connector.mock_data = {
        "oversold": full_data_oversold,
        "overbought": full_data_overbought
    }

    def get_historical_data(ticker, period):
        # Default to oversold data, but can be switched in tests
        return connector.current_data

    connector.get_historical_data.side_effect = get_historical_data
    connector.current_data = full_data_oversold # Default

    return connector


# --- Test Cases ---

def test_signal_agent_buy_signal(mock_strategy_file, mock_data_connector):
    """Test if the SignalAgent correctly generates a BUY signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["oversold"]
    agent = SignalAgent(mock_strategy_file, mock_data_connector)
    signal = agent.generate_signal()
    assert signal == "BUY"

def test_signal_agent_sell_signal(mock_strategy_file, mock_data_connector):
    """Test if the SignalAgent correctly generates a SELL signal."""
    mock_data_connector.current_data = mock_data_connector.mock_data["overbought"]
    agent = SignalAgent(mock_strategy_file, mock_data_connector)
    signal = agent.generate_signal()
    assert signal == "SELL"

def test_portfolio_manager_position_sizing():
    """Test the position sizing calculation."""
    pm = PortfolioManager(initial_cash=100000)

    # Risk 1% of 100k portfolio = $1000 risk
    # Risk per unit = 100 - 98 = $2
    # Position size = 1000 / 2 = 500 units
    position_size = pm.calculate_position_size(
        risk_per_trade_percent=1.0,
        entry_price=100.0,
        stop_loss_price=98.0
    )
    assert position_size == 500.0

def test_portfolio_manager_trade_recording():
    """Test that recording a trade correctly updates cash and positions."""
    pm = PortfolioManager(initial_cash=100000)

    # Buy 10 units of TEST at $100
    pm.record_trade(ticker="TEST", side="BUY", units=10, price=100, reason="ENTRY")

    state = pm.get_state()
    assert state['cash'] == 99000 # 100000 - (10 * 100)
    assert "TEST" in state['positions']
    assert state['positions']['TEST']['units'] == 10

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
