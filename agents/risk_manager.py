from typing import Dict, Any
import pandas as pd

from .technical_analyst import TechnicalAnalyst

class RiskManager:
    """
    A specialized agent for handling all risk management calculations, such as
    stop-loss and take-profit levels, based on the loaded strategy.
    """

    def __init__(self, technical_analyst: TechnicalAnalyst):
        """
        Initializes the RiskManager with the technical analyst.

        Args:
            technical_analyst (TechnicalAnalyst): The agent for indicator calculations.
        """
        self.technical_analyst = technical_analyst

    def calculate_stop_loss(self, strategy: Dict[str, Any], data: pd.DataFrame, entry_price: float) -> float:
        """
        Calculates the stop-loss price based on the strategy's definition.

        Args:
            strategy (Dict[str, Any]): The active strategy dictionary.
            data (pd.DataFrame): The historical market data.
            entry_price (float): The entry price of the potential trade.

        Returns:
            The calculated stop-loss price.
        """
        risk_params = strategy['risk_management']
        method = risk_params.get('stop_loss_method', 'fixed_percent') # Default for safety

        if method == 'atr':
            atr_multiplier = risk_params.get('stop_loss_atr_multiplier', 2.0)
            atr_period = strategy['parameters'].get('atr_period', 14) # Assume ATR period from params

            # Calculate ATR using the TechnicalAnalyst
            data['atr'] = self.technical_analyst.calculate_indicator(
                indicator_name='atr',
                data=data,
                params={'atr_period': atr_period}
            )
            latest_atr = data['atr'].iloc[-1]

            if pd.isna(latest_atr):
                raise ValueError("Could not calculate ATR. Not enough data.")

            stop_loss = entry_price - (latest_atr * atr_multiplier)
            print(f"RiskManager (ATR): Entry=${entry_price:.2f}, ATR=${latest_atr:.2f}, StopLoss=${stop_loss:.2f}")
            return stop_loss

        elif method == 'fixed_percent':
            stop_loss_percent = risk_params.get('stop_loss_percent', 2.0)
            stop_loss = entry_price * (1 - (stop_loss_percent / 100.0))
            print(f"RiskManager (FixedPercent): Entry=${entry_price:.2f}, StopLoss=${stop_loss:.2f}")
            return stop_loss

        else:
            raise ValueError(f"Unsupported stop loss method: {method}")

    def calculate_take_profit(self, strategy: Dict[str, Any], entry_price: float, stop_loss_price: float) -> float:
        """
        Calculates the take-profit price based on the strategy's definition.

        Args:
            strategy (Dict[str, Any]): The active strategy dictionary.
            entry_price (float): The entry price of the trade.
            stop_loss_price (float): The calculated stop-loss price for the trade.

        Returns:
            The calculated take-profit price.
        """
        risk_params = strategy['risk_management']
        method = risk_params.get('take_profit_method')

        if method == 'risk_reward_ratio':
            risk_per_share = entry_price - stop_loss_price
            reward_ratio = risk_params.get('take_profit_ratio', 1.5)
            take_profit = entry_price + (risk_per_share * reward_ratio)
            print(f"RiskManager (RRR): Entry=${entry_price:.2f}, TakeProfit=${take_profit:.2f}")
            return take_profit

        # If no method is defined, we can assume no take-profit is set.
        # Return a very high number or handle it in the master agent. For now, 0 indicates none.
        return 0.0
