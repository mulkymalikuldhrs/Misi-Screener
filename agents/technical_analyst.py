# agents/technical_analyst.py

import pandas as pd
from typing import Dict, Any
from components import technical_indicators as ti

class TechnicalAnalystAgent:
    """
    Analyzes raw market data to identify technical patterns and calculate indicators.
    """

    def calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculates the Average True Range."""
        return ti.calculate_atr(high, low, close, period)

    def calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculates the Relative Strength Index."""
        return ti.calculate_rsi(close, period)

    def calculate_macd(self, close: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
        """Calculates the MACD indicator."""
        return ti.calculate_macd(close, fast_period, slow_period, signal_period)

    def analyze(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Produces a technical analysis report.
        Args:
            market_data: DataFrame with ['High', 'Low', 'Close'] columns.
        """
        atr = self.calculate_atr(market_data['High'], market_data['Low'], market_data['Close'])
        rsi = self.calculate_rsi(market_data['Close'])
        macd_df = self.calculate_macd(market_data['Close'])

        latest_rsi = rsi.iloc[-1]
        latest_macd_hist = macd_df['histogram'].iloc[-1]

        momentum_outlook = "Neutral"
        if latest_rsi > 70 and latest_macd_hist > 0:
            momentum_outlook = "Strong Bullish"
        elif latest_rsi < 30 and latest_macd_hist < 0:
            momentum_outlook = "Strong Bearish"

        return {
            "volatility": {"atr_14": atr.iloc[-1]},
            "momentum": {"rsi_14": latest_rsi, "summary": momentum_outlook},
            "trend": {"summary": "Trending Up" if latest_macd_hist > 0 else "Trending Down"}
        }
