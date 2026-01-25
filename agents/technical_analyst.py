import pandas as pd
from typing import Dict, Any

class TechnicalAnalyst:
    """
    A specialized agent responsible for all technical analysis calculations.
    This decouples the indicator logic from the agents that use them.
    """

    def calculate_indicator(self, indicator_name: str, data: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        """
        Calculates a technical indicator based on its name and parameters.
        This acts as a facade to the underlying calculation methods.
        """
        if indicator_name.lower() == 'rsi':
            return self._calculate_rsi(data, period=params.get('rsi_period', 14))
        elif indicator_name.lower() == 'atr':
            return self._calculate_atr(data, period=params.get('atr_period', 14))
        else:
            raise ValueError(f"Indicator '{indicator_name}' is not supported.")

    def _calculate_rsi(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculates the Relative Strength Index (RSI)."""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_atr(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculates the Average True Range (ATR)."""
        high_low = data['High'] - data['Low']
        high_close = (data['High'] - data['Close'].shift()).abs()
        low_close = (data['Low'] - data['Close'].shift()).abs()

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
