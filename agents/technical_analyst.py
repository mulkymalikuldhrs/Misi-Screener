# agents/technical_analyst.py
import pandas as pd
from components import technical_indicators as ti

class TechnicalAnalyst:
    """
    A specialized agent that contains the logic for all technical indicator calculations.
    This decouples the indicator logic from the agents that use it (e.g., SignalAgent).
    """

    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI).

        Args:
            data (pd.DataFrame): DataFrame with a 'Close' column.
            period (int): The lookback period for RSI calculation.

        Returns:
            A pandas Series containing the RSI values.
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculates the Average True Range (ATR).
        This can be used for dynamic stop-loss calculations.

        Args:
            high (pd.Series): High prices.
            low (pd.Series): Low prices.
            close (pd.Series): Closing prices.
            period (int): The lookback period.

        Returns:
            A pandas Series containing the ATR values.
        """
        high_low = high - low
        high_close = (high - close.shift()).abs()
        low_close = (low - close.shift()).abs()
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr
