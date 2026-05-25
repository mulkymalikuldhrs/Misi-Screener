import time
import asyncio
import datetime
import pytz
from typing import Any
from utils.logger import logger

class HedgeFundMasterAgent:
    """
    The master agent that orchestrates the entire autonomous trading loop.
    This agent is a pure orchestrator, delegating tasks to specialized sub-agents.
    """

    def __init__(self, strategy_manager: Any, signal_agent: Any, portfolio_manager: Any, risk_manager: Any, broker: Any):
        """
        Initializes the master agent with all necessary components.

        Args:
            strategy_manager (Any): Instance of StrategyManager.
            signal_agent (Any): Instance of SignalAgent.
            portfolio_manager (Any): Instance of PortfolioManager.
            risk_manager (Any): Instance of RiskManager.
            broker (Any): Instance of the execution broker.
        """
        self.strategy_manager = strategy_manager
        self.signal_agent = signal_agent
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.broker = broker
        self._is_running = False
        self._task = None

    def is_market_open(self) -> bool:
        """Checks if the US stock market is currently open."""
        tz = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz)

        # Market is open Monday-Friday
        if now.weekday() >= 5: # Saturday or Sunday
            return False

        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

        return market_open <= now <= market_close

    async def run_trading_loop(self):
        """
        Executes a single iteration of the trading loop for all assets in the strategy.
        """
        logger.info("Running trading loop iteration...")

        if not self.is_market_open():
            logger.info("Market is currently closed. Skipping iteration.")
            return

        tickers = self.strategy_manager.get_asset_tickers()
        risk_params = self.strategy_manager.get_risk_management_rules()

        for ticker in tickers:
            try:
                logger.info(f"Processing {ticker}...")
                signal = self.signal_agent.generate_signal(ticker)

                if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
                    logger.info(f"BUY signal received for {ticker}.")
                    entry_price = self.portfolio_manager.get_current_price(ticker)
                    stop_loss_price = self.risk_manager.calculate_stop_loss(ticker, entry_price, risk_params)

                    position_size_units = self.portfolio_manager.calculate_position_size(
                        risk_per_trade_percent=risk_params['risk_per_trade_percent'],
                        entry_price=entry_price,
                        stop_loss_price=stop_loss_price
                    )

                    if position_size_units > 0:
                        logger.info(f"Position size calculated: {position_size_units:.4f} units.")
                        await self.broker.execute_order(ticker, "BUY", position_size_units)
                    else:
                        logger.warning(f"Position size is 0 for {ticker}. No trade executed.")

                elif signal == "SELL" and ticker in self.portfolio_manager.positions:
                    logger.info(f"SELL signal received for {ticker}. Closing position.")
                    units_to_sell = self.portfolio_manager.positions[ticker]['units']
                    await self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
                else:
                    logger.info(f"HOLD or no actionable signal for {ticker}.")

            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")

    async def _start_loop(self, interval_seconds: int):
        """The asynchronous core of the trading loop."""
        self._is_running = True
        logger.info(f"HedgeFundMasterAgent started. Loop will run every {interval_seconds} seconds.")
        while self._is_running:
            try:
                await self.run_trading_loop()
            except Exception as e:
                logger.error(f"Error in main trading loop: {e}")
            await asyncio.sleep(interval_seconds)

    def start(self, interval_seconds: int = 60):
        """
        Starts the autonomous trading loop in a non-blocking manner.
        """
        if not self._is_running:
            self._task = asyncio.create_task(self._start_loop(interval_seconds))

    def stop(self):
        """Stops the trading loop gracefully."""
        if self._is_running and self._task:
            logger.info("HedgeFundMasterAgent stopping...")
            self._is_running = False
            self._task.cancel()
            self._task = None
