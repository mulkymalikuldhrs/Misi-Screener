import yaml
import pandas as pd
from typing import Dict, Any, Optional
from agents.technical_analyst import TechnicalAnalyst

class SignalAgent:
    """
    Generates trading signals based on a defined strategy YAML file.
    It is strategy-agnostic and delegates all technical indicator calculations
    to the TechnicalAnalyst.
    """

    def __init__(self, strategy_filepath: str, data_connector: Any):
        """
        Initializes the agent with a strategy file and a data connector.

        Args:
            strategy_filepath (str): The path to the strategy YAML file.
            data_connector (Any): An instance of a data connector.
        """
        self.strategy = self._load_strategy(strategy_filepath)
        self.data_connector = data_connector
        self.technical_analyst = TechnicalAnalyst()

    def _load_strategy(self, filepath: str) -> Dict[str, Any]:
        """Loads and parses the strategy YAML file."""
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading strategy file {filepath}: {e}")
            raise

    def generate_signal(self) -> Optional[str]:
        """
        Generates a trading signal (BUY, SELL, HOLD) based on the strategy logic.

        Returns:
            A string representing the signal, or None if data is insufficient.
        """
        ticker = self.strategy['asset_ticker']
        fetch_period = "3mo"
        data = self.data_connector.get_historical_data(ticker, period=fetch_period)

        if data.empty:
            print(f"SignalAgent: Could not fetch data for {ticker}.")
            return None

        # --- Delegate Indicator Calculation ---
        params = self.strategy['parameters']
        data['rsi'] = self.technical_analyst.calculate_rsi(data, period=params['rsi_period'])

        # --- Strategy Logic ---
        latest_rsi = data['rsi'].iloc[-1]

        if pd.isna(latest_rsi):
            print("SignalAgent: Not enough data to compute a signal.")
            return None

        print(f"SignalAgent: Latest RSI for {ticker} is {latest_rsi:.2f}")

        # Generate signal based on thresholds
        if latest_rsi < params['oversold_threshold']:
            return "BUY"
        elif latest_rsi > params['overbought_threshold']:
            return "SELL"
        else:
            return "HOLD"
