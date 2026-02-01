import yaml
import pandas as pd
from typing import Dict, Any, Optional

class SignalAgent:
    """
    Generates trading signals based on a defined strategy and technical indicators.
    """

    def __init__(self, strategy_manager: Any, data_connector: Any, technical_analyst: Any):
        """
        Initializes the agent.

        Args:
            strategy_manager (Any): Instance of StrategyManager.
            data_connector (Any): Instance of a data connector (e.g., YFinanceConnector).
            technical_analyst (Any): Instance of TechnicalAnalystAgent.
        """
        self.strategy_manager = strategy_manager
        self.data_connector = data_connector
        self.technical_analyst = technical_analyst

    def generate_signal(self) -> str:
        """
        Generates a trading signal (BUY, SELL, HOLD).
        """
        ticker = self.strategy_manager.get_asset_ticker()
        params = self.strategy_manager.get_strategy_parameters()

        # Fetch historical data
        fetch_period = "3mo"
        data = self.data_connector.get_historical_data(ticker, period=fetch_period)

        if data.empty:
            print(f"SignalAgent: Could not fetch data for {ticker}.")
            return "HOLD"

        # Delegate RSI calculation to TechnicalAnalyst
        rsi_series = self.technical_analyst.calculate_rsi(
            close=data['Close'],
            period=params.get('rsi_period', 14)
        )

        latest_rsi = rsi_series.iloc[-1]

        if latest_rsi is None or pd.isna(latest_rsi):
            return "HOLD"

        print(f"SignalAgent: Latest RSI for {ticker} is {latest_rsi:.2f}")

        if latest_rsi < params.get('oversold_threshold', 30):
            return "BUY"
        elif latest_rsi > params.get('overbought_threshold', 70):
            return "SELL"
        else:
            return "HOLD"
