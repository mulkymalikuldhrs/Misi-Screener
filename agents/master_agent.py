import asyncio
import time
from typing import Any, Dict
from agents.signal_agent import SignalAgent
from agents.portfolio_manager import PortfolioManager
from agents.risk_manager import RiskManager
from execution.paper_trading_broker import PaperTradingBroker

class HedgeFundMasterAgent:
    """
    The master agent that orchestrates the entire autonomous trading loop.
    This agent is a pure orchestrator and delegates all specialized tasks.
    Its trading loop is non-blocking, using asyncio.
    """

    def __init__(self, signal_agent: SignalAgent, portfolio_manager: PortfolioManager, risk_manager: RiskManager, broker: PaperTradingBroker, strategy: Dict[str, Any]):
        self.signal_agent = signal_agent
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.broker = broker
        self.strategy = strategy
        self.is_running = False
        self.task = None

    async def run_trading_loop(self):
        """
        Executes a single iteration of the trading loop.
        """
        print("\n" + "="*50)
        print(f"MasterAgent: Running trading loop iteration at {time.ctime()}")

        signal = self.signal_agent.generate_signal()
        ticker = self.strategy['asset_ticker']

        if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
            print(f"MasterAgent: BUY signal received for {ticker}.")
            try:
                entry_price = self.broker.get_current_price(ticker)
                stop_loss_price = self.risk_manager.calculate_stop_loss(self.strategy, entry_price)

                position_size_units = self.portfolio_manager.calculate_position_size(
                    risk_per_trade_percent=self.strategy['risk_management']['risk_per_trade_percent'],
                    entry_price=entry_price,
                    stop_loss_price=stop_loss_price
                )

                if position_size_units > 0:
                    print(f"MasterAgent: Position size calculated: {position_size_units:.4f} units.")
                    self.broker.execute_order(ticker, "BUY", position_size_units)
                else:
                    print("MasterAgent: Position size is 0. No trade will be executed.")

            except ValueError as e:
                print(f"MasterAgent: Error during trade execution: {e}")

        elif signal == "SELL" and ticker in self.portfolio_manager.positions:
            print(f"MasterAgent: SELL signal received for {ticker}. Closing position.")
            units_to_sell = self.portfolio_manager.positions[ticker]['units']
            self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
        else:
            print(f"MasterAgent: {signal} signal received for {ticker}. No action taken.")

        print("="*50 + "\n")

    async def start(self, interval_seconds: int = 60):
        """
        Starts the autonomous trading loop in a non-blocking manner.
        """
        self.is_running = True
        print(f"HedgeFundMasterAgent started. Loop will run every {interval_seconds} seconds.")
        while self.is_running:
            await self.run_trading_loop()
            await asyncio.sleep(interval_seconds)

    def start_in_background(self, interval_seconds: int = 60):
        """Creates and runs the trading loop as a background task."""
        self.task = asyncio.create_task(self.start(interval_seconds))

    def stop(self):
        """Stops the trading loop."""
        print("HedgeFundMasterAgent stopping...")
        self.is_running = False
        if self.task:
            self.task.cancel()
