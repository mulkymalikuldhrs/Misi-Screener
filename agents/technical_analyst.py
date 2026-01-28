import pandas as pd

class TechnicalAnalyst:
    """
    A specialized agent that contains the logic for all technical indicator calculations.
    This decouples indicator logic from agents that use it (e.g., SignalAgent).
    """

    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI).

        Args:
            data (pd.DataFrame): DataFrame with a 'Close' column.
            period (int): The period for the RSI calculation.

        Returns:
            pd.Series: A series containing the RSI values.
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculates the Average True Range (ATR).

        Args:
            data (pd.DataFrame): DataFrame with 'High', 'Low', 'Close' columns.
            period (int): The period for the ATR calculation.

        Returns:
            pd.Series: A series containing the ATR values.
        """
        high_low = data['High'] - data['Low']
        high_close = (data['High'] - data['Close'].shift()).abs()
        low_close = (data['Low'] - data['Close'].shift()).abs()

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)

        atr = true_range.rolling(window=period).mean()
        return atr
