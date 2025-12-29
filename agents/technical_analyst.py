# agents/technical_analyst.py

from components import technical_indicators as ti

class TechnicalAnalystAgent:
    """
    Analyzes raw market data to identify technical patterns, trends,
    and calculate a wide range of indicators. This agent acts as a coordinator,
    using the 'toolbox' in the components directory to perform calculations.
    """
    def __init__(self):
        """
        Initializes the agent. In a real scenario, this could be configured
        with specific parameters for the indicators.
        """
        self.default_periods = {
            "atr": 14,
            "rsi": 14,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9
        }

    def analyze(self, market_data):
        """
        Takes in market data and produces a technical analysis report.

        Args:
            market_data: A pandas DataFrame with columns ['high', 'low', 'close'].

        Returns:
            A dictionary summarizing the technical outlook.
        """
        # --- 1. Calculate Indicators ---
        atr = ti.calculate_atr(
            high=market_data['high'],
            low=market_data['low'],
            close=market_data['close'],
            period=self.default_periods["atr"]
        )

        rsi = ti.calculate_rsi(
            close=market_data['close'],
            period=self.default_periods["rsi"]
        )

        macd_df = ti.calculate_macd(
            close=market_data['close'],
            fast_period=self.default_periods["macd_fast"],
            slow_period=self.default_periods["macd_slow"],
            signal_period=self.default_periods["macd_signal"]
        )

        # --- 2. Interpret and Structure the Report (Simple Interpretation for now) ---
        # The AI's "thinking" would happen here or in the TraderAgent.
        # This is a simplified interpretation based on the latest values.
        latest_rsi = rsi.iloc[-1]
        latest_macd_hist = macd_df['histogram'].iloc[-1]

        momentum_outlook = "Neutral"
        if latest_rsi > 70 and latest_macd_hist > 0:
            momentum_outlook = "Strong Bullish"
        elif latest_rsi < 30 and latest_macd_hist < 0:
            momentum_outlook = "Strong Bearish"
        elif latest_rsi > 50 and latest_macd_hist > 0:
            momentum_outlook = "Bullish"
        elif latest_rsi < 50 and latest_macd_hist < 0:
            momentum_outlook = "Bearish"

        report = {
            "volatility": {
                "atr_14": atr.iloc[-1]
            },
            "momentum": {
                "rsi_14": latest_rsi,
                "macd_histogram": latest_macd_hist,
                "summary": momentum_outlook
            },
            "trend": {
                "macd_line": macd_df['macd_line'].iloc[-1],
                "signal_line": macd_df['signal_line'].iloc[-1],
                "summary": "Trending Up" if macd_df['macd_line'].iloc[-1] > macd_df['signal_line'].iloc[-1] else "Trending Down"
            }
        }

        return report
