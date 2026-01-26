import yaml
import pandas as pd
from typing import Dict, Any, Optional
from agents.technical_analyst import TechnicalAnalyst

class SignalAgent:
    """
    Generates trading signals based on a defined strategy YAML file.
    It is strategy-agnostic and relies on the TechnicalAnalyst for all indicator calculations.
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

        # --- Strategy Logic ---
        params = self.strategy['parameters']
        # Delegate RSI calculation to the TechnicalAnalyst
        data['rsi'] = self.technical_analyst.calculate_rsi(data, period=params['rsi_period'])

        latest_rsi = data['rsi'].iloc[-1]

        if pd.isna(latest_rsi):
            print("SignalAgent: Not enough data to compute a signal.")
            return None

        print(f"SignalAgent: Latest RSI for {ticker} is {latest_rsi:.2f}")

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
