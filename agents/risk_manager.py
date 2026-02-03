from typing import Dict, Any
from utils.logger import logger

class RiskManager:
    """
    Handles all risk management calculations, including stop-loss placement
    and trade evaluation. This class centralizes risk logic, ensuring
    consistent application of risk rules across the system.
    """

    def __init__(self, data_connector: Any, technical_analyst: Any):
        """
        Initializes the RiskManager.

        Args:
            data_connector (Any): An instance of a data connector to fetch market data.
            technical_analyst (Any): An instance of the TechnicalAnalyst for indicator calculations.
        """
        self.data_connector = data_connector
        self.technical_analyst = technical_analyst

    def calculate_stop_loss(self, ticker: str, entry_price: float, risk_params: Dict[str, Any]) -> float:
        """
        Calculates the stop-loss price based on the specified method in the strategy.

        Args:
            ticker (str): The asset ticker.
            entry_price (float): The entry price of the trade.
            risk_params (Dict[str, Any]): The risk management rules from the strategy.

        Returns:
            The calculated stop-loss price.
        """
        method = risk_params.get('stop_loss_method', 'fixed_percent')

        if method == 'atr':
            return self._calculate_atr_stop_loss(ticker, entry_price, risk_params)
        elif method == 'fixed_percent':
            return self._calculate_fixed_percent_stop_loss(entry_price, risk_params)
        else:
            logger.warning(f"Unknown stop-loss method '{method}'. Defaulting to fixed percent.")
            return self._calculate_fixed_percent_stop_loss(entry_price, risk_params)

    def _calculate_fixed_percent_stop_loss(self, entry_price: float, risk_params: Dict[str, Any]) -> float:
        """Calculates a stop-loss based on a fixed percentage."""
        percent = risk_params.get('stop_loss_percent', 2.0)
        return entry_price * (1 - (percent / 100.0))

    def _calculate_atr_stop_loss(self, ticker: str, entry_price: float, risk_params: Dict[str, Any]) -> float:
        """
        Calculates a stop-loss based on the Average True Range (ATR), a measure of volatility.
        """
        atr_multiplier = risk_params.get('atr_multiplier', 2.0)
        atr_period = risk_params.get('atr_period', 14)

        # Fetch historical data to calculate ATR
        data = self.data_connector.get_historical_data(ticker, period="3mo")
        if data.empty:
            logger.warning(f"Could not fetch data for {ticker}. Using fixed percent stop-loss.")
            return self._calculate_fixed_percent_stop_loss(entry_price, risk_params)

        # Use the technical analyst to calculate ATR
        atr_series = self.technical_analyst.calculate_atr(
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            period=atr_period
        )
        latest_atr = atr_series.iloc[-1]

        stop_loss_price = entry_price - (latest_atr * atr_multiplier)
        return stop_loss_price
