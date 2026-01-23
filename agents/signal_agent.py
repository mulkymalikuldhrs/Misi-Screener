import pandas as pd
from typing import Dict, Any, Optional

class SignalAgent:
    """
    Generates trading signals based on a strategy configuration and technical analysis.
    This agent is strategy-agnostic and relies on a TechnicalAnalyst for indicator calculations.
    """

    def __init__(self, strategy: Dict[str, Any], data_connector: Any, technical_analyst: Any):
        """
        Initializes the agent with a strategy config, a data connector, and a technical analyst.

        Args:
            strategy (Dict[str, Any]): The strategy configuration dictionary.
            data_connector (Any): An instance of a data connector.
            technical_analyst (Any): An instance of the TechnicalAnalyst.
        """
        self.strategy = strategy
        self.data_connector = data_connector
        self.technical_analyst = technical_analyst

    def generate_signal(self) -> Optional[str]:
        """
        Generates a trading signal (BUY, SELL, HOLD) based on the strategy logic.

        Returns:
            A string representing the signal, or None if data is insufficient.
        """
        ticker = self.strategy['asset_ticker']
        params = self.strategy['parameters']
        indicator_name = params.get('indicator', 'rsi')

        # Fetch historical data
        fetch_period = "3mo"  # A reasonable lookback
        data = self.data_connector.get_historical_data(ticker, period=fetch_period)

        if data.empty:
            print(f"SignalAgent: Could not fetch data for {ticker}.")
            return None

        # Delegate indicator calculation to the TechnicalAnalyst
        if indicator_name == 'rsi':
            indicator_series = self.technical_analyst.calculate_rsi(data, params['rsi_period'])
        else:
            print(f"SignalAgent: Indicator '{indicator_name}' is not supported.")
            return None

        latest_indicator_value = indicator_series.iloc[-1]

        if pd.isna(latest_indicator_value):
            print("SignalAgent: Not enough data to compute a signal.")
            return None

        print(f"SignalAgent: Latest {indicator_name.upper()} for {ticker} is {latest_indicator_value:.2f}")

        # Generate signal based on strategy thresholds
        if latest_indicator_value < params['oversold_threshold']:
            return "BUY"
        elif latest_indicator_value > params['overbought_threshold']:
            return "SELL"
        else:
            return "HOLD"
