from typing import Dict, Any
import pandas as pd
from agents.technical_analyst import TechnicalAnalyst

class RiskManager:
    """
    A specialized agent dedicated to handling all risk management calculations,
    such as ATR-based stop-loss and take-profit levels.
    """

    def __init__(self, technical_analyst: TechnicalAnalyst, data_connector: Any):
        """
        Initializes the RiskManager.

        Args:
            technical_analyst (TechnicalAnalyst): Instance for indicator calculations.
            data_connector (Any): Instance for fetching market data.
        """
        self.technical_analyst = technical_analyst
        self.data_connector = data_connector

    def calculate_stop_loss(self, strategy: Dict[str, Any], entry_price: float, data: pd.DataFrame) -> float:
        """
        Calculates the stop-loss price based on the strategy's risk parameters.

        Args:
            strategy (Dict[str, Any]): The strategy definition.
            entry_price (float): The entry price of the asset.
            data (pd.DataFrame): The historical data for the asset.

        Returns:
            float: The calculated stop-loss price.
        """
        risk_params = strategy['risk_management']
        method = risk_params.get('stop_loss_method')

        if method == 'atr':
            atr_period = risk_params.get('stop_loss_atr_period', 14)
            atr_multiplier = risk_params.get('stop_loss_atr_multiplier', 2.0)
            data['atr'] = self.technical_analyst.calculate_atr(data, period=atr_period)
            latest_atr = data['atr'].iloc[-1]

            if pd.isna(latest_atr):
                # Fallback if ATR is not available
                return self.calculate_fallback_stop_loss(entry_price, risk_params)

            stop_loss_price = entry_price - (latest_atr * atr_multiplier)
            print(f"RiskManager (ATR): Entry=${entry_price:.2f}, ATR={latest_atr:.2f}, StopLoss=${stop_loss_price:.2f}")
            return stop_loss_price

        elif method == 'fixed_percent':
            return entry_price * (1 - (risk_params.get('stop_loss_percent', 2.0) / 100.0))

        # Default fallback
        return self.calculate_fallback_stop_loss(entry_price, risk_params)

    def calculate_fallback_stop_loss(self, entry_price: float, risk_params: Dict[str, Any]) -> float:
        """A default fixed-percentage stop-loss as a fallback."""
        percent = risk_params.get('stop_loss_percent', 2.0)
        fallback_price = entry_price * (1 - (percent / 100.0))
        print(f"RiskManager (Fallback): Using fixed {percent}% stop loss -> ${fallback_price:.2f}")
        return fallback_price
