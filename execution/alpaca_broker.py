import os
import asyncio
import alpaca_trade_api as tradeapi
from typing import Any
from utils.logger import logger

class AlpacaBroker:
    """
    A real broker connector for Alpaca. Supports both paper and live trading.
    """

    def __init__(self, portfolio_manager: Any, api_key: str = None, api_secret: str = None, base_url: str = None):
        """
        Initializes the Alpaca broker.
        """
        self.portfolio_manager = portfolio_manager

        self.api_key = api_key or os.environ.get('ALPACA_API_KEY')
        self.api_secret = api_secret or os.environ.get('ALPACA_API_SECRET')
        self.base_url = base_url or os.environ.get('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

        if not self.api_key or not self.api_secret:
            logger.error("AlpacaBroker Error: API credentials not found.")
            self.api = None
        else:
            try:
                self.api = tradeapi.REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
                account = self.api.get_account()
                logger.info(f"AlpacaBroker: Connected to Alpaca. Account Status: {account.status}")
            except Exception as e:
                logger.error(f"AlpacaBroker Error: Could not connect to Alpaca: {e}")
                self.api = None

    async def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY"):
        """
        Executes an order on Alpaca and records it in the portfolio manager.
        """
        if self.api is None:
            logger.error(f"AlpacaBroker Error: Cannot execute {side} {units} {ticker} without API connection.")
            raise ConnectionError("No connection to Alpaca API.")

        try:
            logger.info(f"AlpacaBroker: Submitting {side} order for {units:.4f} {ticker}...")

            # submit_order is a blocking call in the SDK, but it's relatively fast.
            # To be truly non-blocking, we could run it in a threadpool.
            # However, the polling loop is the real culprit.
            order = await asyncio.to_thread(
                self.api.submit_order,
                symbol=ticker,
                qty=units,
                side=side.lower(),
                type='market',
                time_in_force='gtc'
            )

            # Polling for fill (non-blocking)
            filled = False
            for _ in range(30): # Try for 30 seconds
                order = await asyncio.to_thread(self.api.get_order, order.id)
                if order.status == 'filled':
                    filled = True
                    break
                await asyncio.sleep(1) # Non-blocking sleep

            if filled:
                execution_price = float(order.filled_avg_price)
                actual_units = float(order.filled_qty)
                logger.info(f"AlpacaBroker: Order filled. {side} {actual_units} {ticker} @ ${execution_price:.2f}")

                self.portfolio_manager.record_trade(
                    ticker=ticker,
                    side=side,
                    units=actual_units,
                    price=execution_price,
                    reason=reason
                )
            else:
                logger.warning(f"AlpacaBroker: Order {order.id} not filled yet. Status: {order.status}")

        except Exception as e:
            logger.error(f"AlpacaBroker Error during order execution: {e}")
            raise
