import time
import asyncio
from typing import Any

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

    def run_trading_loop(self):
        """
        Executes a single iteration of the trading loop.
        This function is called repeatedly by the asyncio scheduler.
        """
        print("\n" + "=" * 50)
        print(f"MasterAgent: Running trading loop iteration at {time.ctime()}")

        signal = self.signal_agent.generate_signal()
        ticker = self.strategy_manager.get_asset_ticker()
        risk_params = self.strategy_manager.get_risk_management_rules()

        if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
            print(f"MasterAgent: BUY signal received for {ticker}.")
            try:
                entry_price = self.portfolio_manager.get_current_price(ticker)
                stop_loss_price = self.risk_manager.calculate_stop_loss(ticker, entry_price, risk_params)

                position_size_units = self.portfolio_manager.calculate_position_size(
                    risk_per_trade_percent=risk_params['risk_per_trade_percent'],
                    entry_price=entry_price,
                    stop_loss_price=stop_loss_price
                )

                if position_size_units > 0:
                    print(f"MasterAgent: Position size calculated: {position_size_units:.4f} units.")
                    self.broker.execute_order(ticker, "BUY", position_size_units)
                else:
                    print("MasterAgent: Position size is 0 or invalid. No trade will be executed.")
            except ValueError as e:
                print(f"MasterAgent Error: {e}")

        elif signal == "SELL" and ticker in self.portfolio_manager.positions:
            print(f"MasterAgent: SELL signal received for {ticker}. Closing position.")
            units_to_sell = self.portfolio_manager.positions[ticker]['units']
            self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
        else:
            print(f"MasterAgent: HOLD signal received for {ticker}. No action taken.")

        print("=" * 50 + "\n")

    async def _start_loop(self, interval_seconds: int):
        """The asynchronous core of the trading loop."""
        self._is_running = True
        print(f"HedgeFundMasterAgent started. Loop will run every {interval_seconds} seconds.")
        while self._is_running:
            self.run_trading_loop()
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
            print("HedgeFundMasterAgent stopping...")
            self._is_running = False
            self._task.cancel()
            self._task = None
