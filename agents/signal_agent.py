import pandas as pd
from typing import Dict, Any, Optional

# Import the new TechnicalAnalyst
from .technical_analyst import TechnicalAnalyst

class SignalAgent:
    """
    Generates trading signals based on a strategy dictionary, using a TechnicalAnalyst
    for all indicator calculations. This agent is now strategy-agnostic.
    """

    def __init__(self, strategy: Dict[str, Any], data_connector: Any, technical_analyst: TechnicalAnalyst):
        """
        Initializes the agent with a strategy, data connector, and technical analyst.

        Args:
            strategy (Dict[str, Any]): The loaded strategy definition.
            data_connector (Any): An instance of a data connector.
            technical_analyst (TechnicalAnalyst): An instance of the technical analyst agent.
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

        # Fetch the required historical data
        fetch_period = "3mo" # A reasonable lookback for most indicators
        data = self.data_connector.get_historical_data(ticker, period=fetch_period)

        if data.empty:
            print(f"SignalAgent: Could not fetch data for {ticker}.")
            return None

        # --- Strategy Logic ---
        # The agent is now agnostic to the indicator being used. It just calculates
        # whatever is specified in the strategy file.
        params = self.strategy['parameters']
        indicator_name = params.get('indicator', 'rsi') # Default to rsi for backward compatibility

        data[indicator_name] = self.technical_analyst.calculate_indicator(
            indicator_name=indicator_name,
            data=data,
            params=params
        )

        # Get the most recent indicator value
        latest_indicator_value = data[indicator_name].iloc[-1]

        if latest_indicator_value is None or pd.isna(latest_indicator_value):
            print("SignalAgent: Not enough data to compute a signal.")
            return None

        print(f"SignalAgent: Latest {indicator_name.upper()} for {ticker} is {latest_indicator_value:.2f}")

        # Generate signal based on thresholds
        if latest_indicator_value < params['oversold_threshold']:
            return "BUY"
        elif latest_indicator_value > params['overbought_threshold']:
            return "SELL"
        else:
            return "HOLD"
