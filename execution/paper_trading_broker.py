import asyncio
from typing import Dict, Any
from utils.logger import logger

class PaperTradingBroker:
    """
    A simulated broker for paper trading. It simulates order execution.
    """

    def __init__(self, portfolio_manager: Any, data_connector: Any, slippage_percent: float = 0.0, commission_fee: float = 0.0):
        """
        Initializes the broker.
        """
        self.portfolio_manager = portfolio_manager
        self.data_connector = data_connector
        self.slippage_percent = slippage_percent
        self.commission_fee = commission_fee

    def _get_current_price(self, ticker: str) -> float:
        """Fetches the most recent closing price for an asset."""
        data = self.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"PaperTradingBroker: Could not get current price for {ticker}.")
        return data['Close'].iloc[-1]

    async def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY"):
        """
        Simulates the execution of a market order.
        """
        if units <= 0:
            return

        try:
            # Simulate a small network delay
            await asyncio.sleep(0.1)

            base_price = self._get_current_price(ticker)

            # Apply slippage
            slippage_factor = 1 + (self.slippage_percent / 100.0) if side == "BUY" else 1 - (self.slippage_percent / 100.0)
            execution_price = base_price * slippage_factor

            logger.info(f"PaperTradingBroker: Executing {side} order for {units:.4f} {ticker} at simulated price ${execution_price:.2f}.")

            # Record the executed trade with the portfolio manager
            self.portfolio_manager.record_trade(
                ticker=ticker,
                side=side,
                units=units,
                price=execution_price,
                reason=reason
            )

        except Exception as e:
            logger.error(f"PaperTradingBroker Error: {e}")
            raise
