import asyncio
import time
from typing import Any, Dict

class HedgeFundMasterAgent:
    """
    The master agent that orchestrates the entire autonomous trading loop.
    This agent is a pure orchestrator, delegating all specialized tasks
    (strategy, signals, risk, portfolio) to other manager/agent classes.
    Its trading loop is non-blocking, using asyncio.
    """

    def __init__(self, signal_agent: Any, portfolio_manager: Any, risk_manager: Any, broker: Any, strategy: Dict[str, Any]):
        """
        Initializes the master agent with all necessary components.
        """
        self.signal_agent = signal_agent
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.broker = broker
        self.strategy = strategy
        self.is_running = False

    async def run_trading_loop(self):
        """
        Executes a single, non-blocking iteration of the trading loop.
        """
        print("\n" + "="*50)
        print(f"MasterAgent: Running trading loop iteration at {time.ctime()}")

        signal = self.signal_agent.generate_signal()
        ticker = self.strategy['asset_ticker']

        if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
            print(f"MasterAgent: BUY signal received for {ticker}.")
            try:
                # Fetch data needed for risk calculation
                data = self.signal_agent.data_connector.get_historical_data(ticker, period="3mo")
                if data.empty:
                    print("MasterAgent: Could not fetch data for BUY execution. Skipping.")
                    return

                entry_price = data['Close'].iloc[-1]

                # Delegate stop-loss calculation to RiskManager
                stop_loss_price = self.risk_manager.calculate_stop_loss(
                    strategy=self.strategy,
                    entry_price=entry_price,
                    data=data
                )

                # Delegate position sizing to PortfolioManager
                position_size_units = self.portfolio_manager.calculate_position_size(
                    risk_per_trade_percent=self.strategy['risk_management']['risk_per_trade_percent'],
                    entry_price=entry_price,
                    stop_loss_price=stop_loss_price
                )

                if position_size_units > 0:
                    print(f"MasterAgent: Sized position: {position_size_units:.4f} units.")
                    self.broker.execute_order(ticker, "BUY", position_size_units)
                else:
                    print("MasterAgent: Position size is 0. No trade executed.")

            except Exception as e:
                print(f"MasterAgent: Error during BUY execution: {e}")

        elif signal == "SELL":
            if ticker in self.portfolio_manager.positions:
                print(f"MasterAgent: SELL signal for {ticker}. Closing position.")
                units_to_sell = self.portfolio_manager.positions[ticker]['units']
                self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
            else:
                print("MasterAgent: SELL signal received, but no open position.")
        else:
            print(f"MasterAgent: HOLD signal received for {ticker}. No action taken.")

        print("="*50 + "\n")

    async def start(self, interval_seconds: int = 60):
        """
        Starts the autonomous, non-blocking trading loop.
        """
        self.is_running = True
        print(f"HedgeFundMasterAgent started. Loop runs every {interval_seconds} seconds.")
        while self.is_running:
            await self.run_trading_loop()
            await asyncio.sleep(interval_seconds)

    def stop(self):
        """Stops the trading loop."""
        print("HedgeFundMasterAgent stopping...")
        self.is_running = False
