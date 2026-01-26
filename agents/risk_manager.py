from typing import Dict, Any
import pandas as pd
from agents.technical_analyst import TechnicalAnalyst

class RiskManager:
    """
    A specialized agent dedicated to handling all risk management calculations,
    such as ATR-based stop-loss. This decouples risk logic from the master agent.
    """

    def __init__(self, technical_analyst: TechnicalAnalyst, data_connector: Any):
        """
        Initializes the RiskManager.

        Args:
            technical_analyst (TechnicalAnalyst): An instance of the technical analyst for ATR calculation.
            data_connector (Any): The data connector to fetch market data.
        """
        self.technical_analyst = technical_analyst
        self.data_connector = data_connector

    def calculate_stop_loss(self, strategy: Dict[str, Any], entry_price: float) -> float:
        """
        Calculates the stop-loss price based on the strategy's risk management rules.

        Args:
            strategy (Dict[str, Any]): The strategy configuration dictionary.
            entry_price (float): The entry price of the asset.

        Returns:
            The calculated stop-loss price.
        """
        risk_params = strategy['risk_management']
        method = risk_params.get('stop_loss_method', 'fixed_percent')

        if method == 'atr':
            ticker = strategy['asset_ticker']
            data = self.data_connector.get_historical_data(ticker, period="3mo")
            if data.empty:
                # Fallback to fixed percent if data is unavailable
                return entry_price * (1 - (risk_params.get('stop_loss_percent', 2.0) / 100.0))

            atr_value = self.technical_analyst.calculate_atr(data['High'], data['Low'], data['Close']).iloc[-1]
            atr_multiplier = risk_params.get('atr_multiplier', 2.0)
            return entry_price - (atr_value * atr_multiplier)

        elif method == 'fixed_percent':
            stop_loss_percent = risk_params.get('stop_loss_percent', 2.0)
            return entry_price * (1 - (stop_loss_percent / 100.0))

        else:
            # Default fallback
            return entry_price * (1 - (2.0 / 100.0))
