import pandas as pd
from components import technical_indicators as ti

class TechnicalAnalyst:
    """
    A facade for the technical indicator calculation library.
    This agent provides a clean, strategy-agnostic interface for other agents
    to retrieve technical analysis data.
    """

    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI).

        Args:
            data (pd.DataFrame): DataFrame with a 'Close' column.
            period (int): The lookback period for the RSI calculation.

        Returns:
            A pandas Series containing the RSI values.
        """
        return ti.calculate_rsi(close=data['Close'], period=period)

    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculates the Average True Range (ATR).

        Args:
            data (pd.DataFrame): DataFrame with 'High', 'Low', 'Close' columns.
            period (int): The lookback period for the ATR calculation.

        Returns:
            A pandas Series containing the ATR values.
        """
        return ti.calculate_atr(high=data['High'], low=data['Low'], close=data['Close'], period=period)

    def calculate_macd(self, data: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
        """
        Calculates the Moving Average Convergence Divergence (MACD).

        Args:
            data (pd.DataFrame): DataFrame with a 'Close' column.
            fast_period (int): Fast EMA period.
            slow_period (int): Slow EMA period.
            signal_period (int): Signal line EMA period.

        Returns:
            A DataFrame with MACD line, signal line, and histogram.
        """
        return ti.calculate_macd(
            close=data['Close'],
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period
        )
