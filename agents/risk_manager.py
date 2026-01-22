from typing import Any
import pandas as pd
import numpy as np

class RiskManager:
    """
    Manages all risk-related calculations for the hedge fund, including
    stop-loss, take-profit, and any other risk overlays.
    """

    def __init__(self, data_connector: Any):
        """
        Initializes the RiskManager.

        Args:
            data_connector: An instance of a data connector (e.g., YFinanceConnector)
                            to fetch the necessary data for calculations like ATR.
        """
        self.data_connector = data_connector

    def _calculate_atr(self, ticker: str, period: int = 14) -> float:
        """
        Calculates the Average True Range (ATR) for a given ticker.

        Args:
            ticker (str): The asset ticker.
            period (int): The lookback period for ATR calculation.

        Returns:
            float: The latest ATR value.
        """
        try:
            # Fetch enough data for the ATR calculation
            df = self.data_connector.get_historical_data(ticker, period=f"{period * 2}d")
            if df.empty or len(df) < period:
                raise ValueError("Not enough historical data for ATR calculation.")

            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())

            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.ewm(com=period - 1, adjust=False).mean()

            latest_atr = atr.iloc[-1]
            if np.isnan(latest_atr):
                 raise ValueError("ATR calculation resulted in NaN.")
            return latest_atr

        except Exception as e:
            print(f"RiskManager: Error calculating ATR for {ticker}: {e}")
            # Fallback to a default value or re-raise
            raise ValueError(f"Could not calculate ATR for {ticker}.") from e


    def calculate_stop_loss(self, strategy_params: dict, ticker: str, entry_price: float) -> float:
        """
        Calculates the stop-loss price based on the method defined in the strategy.

        Args:
            strategy_params (dict): The 'risk_management' section of the strategy YAML.
            ticker (str): The asset ticker.
            entry_price (float): The price at which the asset was entered.

        Returns:
            float: The calculated stop-loss price.
        """
        method = strategy_params.get('stop_loss_method', 'fixed_percent')

        if method == 'atr':
            atr_period = strategy_params.get('atr_period', 14)
            atr_multiplier = strategy_params.get('atr_multiplier', 2.0)

            print(f"RiskManager: Calculating stop-loss using ATR(period={atr_period}, multiplier={atr_multiplier}).")

            atr_value = self._calculate_atr(ticker, period=atr_period)
            stop_loss_price = entry_price - (atr_value * atr_multiplier)

            print(f"RiskManager: ATR={atr_value:.4f}, Stop-Loss Price={stop_loss_price:.2f}")
            return stop_loss_price

        elif method == 'fixed_percent':
            stop_loss_percent = strategy_params.get('stop_loss_percent', 2.0)
            print(f"RiskManager: Calculating stop-loss using fixed {stop_loss_percent}%")
            return entry_price * (1 - (stop_loss_percent / 100.0))

        else:
            raise ValueError(f"Unknown stop_loss_method: '{method}'")
