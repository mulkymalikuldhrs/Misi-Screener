from typing import Dict, Any, Tuple
from utils.logger import logger

class RiskManager:
    """
    Handles all risk management calculations, including stop-loss placement
    and trade evaluation. This class centralizes risk logic, ensuring
    consistent application of risk rules across the system.
    """

    # Maximum percentage of portfolio to allocate to a single position
    MAX_POSITION_PCT = 0.25  # 25%
    # Maximum portfolio heat (sum of all position risks)
    MAX_PORTFOLIO_HEAT_PCT = 0.06  # 6%
    # Maximum daily loss as fraction of portfolio
    MAX_DAILY_LOSS_PCT = 0.03  # 3%

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
        # Support both 'atr_multiplier' and 'stop_loss_atr_multiplier' (YAML key)
        atr_multiplier = risk_params.get('atr_multiplier',
                         risk_params.get('stop_loss_atr_multiplier', 2.0))
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
        logger.info(f"ATR stop-loss for {ticker}: entry={entry_price:.2f}, ATR={latest_atr:.2f}, "
                    f"multiplier={atr_multiplier}, stop={stop_loss_price:.2f}")
        return stop_loss_price

    def evaluate_trade(self, trade_proposal: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Evaluates a proposed trade against risk management rules.

        Args:
            trade_proposal: A dictionary containing the trade details:
                - asset: The ticker symbol
                - action: 'BUY' or 'SELL'
                - entry_price: The intended entry price
                - stop_loss: The stop-loss price
                - position_size: The number of units
                - risk_per_trade: The risk per trade as a fraction

        Returns:
            A tuple of (is_approved: bool, reason: str).
        """
        entry_price = trade_proposal.get('entry_price', 0)
        stop_loss = trade_proposal.get('stop_loss')
        position_size = trade_proposal.get('position_size', 0)
        action = trade_proposal.get('action', '')

        # Rule 1: Must have a stop-loss for BUY orders
        if action == 'BUY' and stop_loss is None:
            return False, "No stop-loss price set. Trade rejected for safety."

        # Rule 2: Stop-loss must be below entry for BUY orders
        if action == 'BUY' and stop_loss is not None and stop_loss >= entry_price:
            return False, f"Stop-loss ({stop_loss:.2f}) must be below entry price ({entry_price:.2f})."

        # Rule 3: Position size must be positive
        if action == 'BUY' and position_size is not None and position_size <= 0:
            return False, "Position size must be positive."

        # Rule 4: Check maximum risk per trade
        risk_per_trade = trade_proposal.get('risk_per_trade')
        if risk_per_trade is not None and risk_per_trade > self.MAX_PORTFOLIO_HEAT_PCT:
            return False, f"Risk per trade ({risk_per_trade:.2%}) exceeds maximum allowed ({self.MAX_PORTFOLIO_HEAT_PCT:.2%})."

        # If all checks pass, approve the trade
        logger.info(f"RiskManager: Trade approved for {trade_proposal.get('asset')} "
                    f"{action} @ {entry_price}")
        return True, "Trade approved by risk management."
