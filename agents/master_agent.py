import asyncio
import time
from typing import Any, Dict

# Import all the new specialized agents
from .strategy_manager import StrategyManager
from .signal_agent import SignalAgent
from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager

class HedgeFundMasterAgent:
    """
    The master agent orchestrator, re-architected to be a pure, non-blocking
    coordinator that delegates tasks to specialized agents.
    """

    def __init__(self,
                 strategy_manager: StrategyManager,
                 signal_agent: SignalAgent,
                 portfolio_manager: PortfolioManager,
                 risk_manager: RiskManager,
                 broker: Any,
                 data_connector: Any):
        """
        Initializes the master agent with all necessary components.
        """
        self.strategy_manager = strategy_manager
        self.signal_agent = signal_agent
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.broker = broker
        self.data_connector = data_connector # Used for fetching latest price data

        self.strategy: Dict[str, Any] = self.strategy_manager.get_strategy()
        self._is_running = False
        self._task = None

    async def _run_trading_loop(self, interval_seconds: int):
        """The core asynchronous trading loop."""
        print(f"HedgeFundMasterAgent started. Loop will run every {interval_seconds} seconds.")
        while self._is_running:
            start_time = time.time()
            print("\n" + "="*50)
            print(f"MasterAgent: Running trading loop iteration at {time.ctime()}")

            # 1. Generate Signal
            signal = self.signal_agent.generate_signal()
            ticker = self.strategy['asset_ticker']

            # 2. Act on Signal
            if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
                print(f"MasterAgent: BUY signal received for {ticker}.")
                await self._handle_buy_signal(ticker)
            elif signal == "SELL":
                await self._handle_sell_signal(ticker)
            else: # HOLD
                print(f"MasterAgent: HOLD signal received for {ticker}. No action taken.")

            # 3. Update Portfolio Valuation
            # This is crucial for accurate, real-time risk management
            self.portfolio_manager.update_market_valuations()
            print(f"MasterAgent: Portfolio value is now ${self.portfolio_manager.get_state()['portfolio_value']:.2f}")


            print("="*50 + "\n")

            # Wait for the next interval
            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, interval_seconds - elapsed_time))

    async def _handle_buy_signal(self, ticker: str):
        """Handles the logic for executing a BUY order."""
        try:
            # Fetch fresh data for risk calculations
            data = self.data_connector.get_historical_data(ticker, period="3mo")
            if data.empty:
                raise ValueError("Could not get data for risk calculation.")

            entry_price = data['Close'].iloc[-1]

            # Delegate risk calculations to the RiskManager
            stop_loss_price = self.risk_manager.calculate_stop_loss(self.strategy, data, entry_price)

            # Delegate position sizing to the PortfolioManager, which now has real-time valuation
            self.portfolio_manager.update_market_valuations() # Ensure valuation is fresh
            position_size_units = self.portfolio_manager.calculate_position_size(
                risk_per_trade_percent=self.strategy['risk_management']['risk_per_trade_percent'],
                entry_price=entry_price,
                stop_loss_price=stop_loss_price
            )

            if position_size_units > 0:
                print(f"MasterAgent: Position size calculated: {position_size_units:.4f} units.")
                self.broker.execute_order(ticker, "BUY", position_size_units, reason="ENTRY")
            else:
                print("MasterAgent: Position size is 0 or less. No trade will be executed.")

        except ValueError as e:
            print(f"MasterAgent Error on BUY: {e}")

    async def _handle_sell_signal(self, ticker: str):
        """Handles the logic for closing a position based on a SELL signal."""
        if ticker in self.portfolio_manager.positions:
            print(f"MasterAgent: SELL signal received for {ticker}. Closing position.")
            units_to_sell = self.portfolio_manager.positions[ticker]['units']
            self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
        else:
            print("MasterAgent: SELL signal received, but no open position to close.")

    def start(self, interval_seconds: int = 60):
        """Starts the autonomous trading loop in the background."""
        if not self._is_running:
            self._is_running = True
            self._task = asyncio.create_task(self._run_trading_loop(interval_seconds))
            print("HedgeFundMasterAgent task created.")

    def stop(self):
        """Stops the trading loop gracefully."""
        if self._is_running and self._task:
            print("HedgeFundMasterAgent stopping...")
            self._is_running = False
            self._task.cancel()
            self._task = None
            print("HedgeFundMasterAgent stopped.")
