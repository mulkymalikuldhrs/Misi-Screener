import yaml
import pandas as pd
from typing import Dict, Any, Optional

class SignalAgent:
    """
    Generates trading signals based on a defined strategy YAML file.
    """

    def __init__(self, strategy_filepath: str, data_connector: Any):
        """
        Initializes the agent with a strategy file and a data connector.

        Args:
            strategy_filepath (str): The path to the strategy YAML file.
            data_connector (Any): An instance of a data connector (e.g., YFinanceConnector).
        """
        self.strategy = self._load_strategy(strategy_filepath)
        self.data_connector = data_connector

    def _load_strategy(self, filepath: str) -> Dict[str, Any]:
        """Loads and parses the strategy YAML file."""
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading strategy file {filepath}: {e}")
            raise

    def _calculate_rsi(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculates the Relative Strength Index (RSI)."""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signal(self) -> Optional[str]:
        """
        Generates a trading signal (BUY, SELL, HOLD) based on the strategy logic.

        Returns:
            A string representing the signal, or None if data is insufficient.
        """
        ticker = self.strategy['asset_ticker']
        timeframe = self.strategy['timeframe']

        # Fetch the required historical data
        # We fetch more data than the RSI period to ensure the calculation is stable
        fetch_period = "3mo" # A reasonable lookback for hourly data
        data = self.data_connector.get_historical_data(ticker, period=fetch_period)

        if data.empty:
            print(f"SignalAgent: Could not fetch data for {ticker}.")
            return None

        # --- Strategy Logic ---
        params = self.strategy['parameters']
        data['rsi'] = self._calculate_rsi(data, params['rsi_period'])

        # Get the most recent RSI value
        latest_rsi = data['rsi'].iloc[-1]

        if latest_rsi is None or pd.isna(latest_rsi):
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

# Example Usage
if __name__ == '__main__':
    # This is a mock connector for testing purposes
    class MockConnector:
        def get_historical_data(self, ticker, period):
            # In a real scenario, this fetches live data
            # For this example, we'll create some dummy data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='1h')
            price = 100
            prices = []
            for _ in range(100):
                price += pd.np.random.randn()
                prices.append(price)
            return pd.DataFrame({'Close': prices}, index=dates)

    # Initialize the agent with the strategy file and a data connector
    strategy_file = '../strategies/mean_reversion_rsi.yml'

    try:
        signal_agent = SignalAgent(strategy_filepath=strategy_file, data_connector=MockConnector())
        signal = signal_agent.generate_signal()
        print(f"\nGenerated Signal: {signal}")
    except Exception as e:
        print(f"Failed to run SignalAgent example: {e}")
