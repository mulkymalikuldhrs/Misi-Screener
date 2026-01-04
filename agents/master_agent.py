import time
from typing import Any

class HedgeFundMasterAgent:
    """
    The master agent that orchestrates the entire autonomous trading loop.
    """

    def __init__(self, signal_agent: Any, portfolio_manager: Any, broker: Any, strategy: dict):
        """
        Initializes the master agent with all necessary components.

        Args:
            signal_agent (Any): Instance of SignalAgent.
            portfolio_manager (Any): Instance of PortfolioManager.
            broker (Any): Instance of PaperTradingBroker.
            strategy (dict): The loaded strategy definition dictionary.
        """
        self.signal_agent = signal_agent
        self.portfolio_manager = portfolio_manager
        self.broker = broker
        self.strategy = strategy
        self.is_running = False

    def _get_current_price(self) -> float:
        """Helper to get the current price for stop-loss calculation."""
        # This is a slight duplication of broker logic, could be refactored.
        ticker = self.strategy['asset_ticker']
        data = self.signal_agent.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"MasterAgent: Could not get current price for {ticker}.")
        return data['Close'].iloc[-1]

    def _calculate_stop_loss(self, entry_price: float) -> float:
        """Calculates stop loss based on the strategy's risk management rules."""
        risk_params = self.strategy['risk_management']
        if risk_params['stop_loss_method'] == 'fixed_percent':
            return entry_price * (1 - (risk_params.get('stop_loss_percent', 2.0) / 100.0))
        # Default to a simple fixed percentage if ATR logic is not implemented yet.
        # TODO: Implement ATR-based stop loss calculation.
        return entry_price * (1 - (2.0 / 100.0)) # Fallback to 2%

    def run_trading_loop(self):
        """
        Executes a single iteration of the trading loop.
        This function will be called repeatedly by a scheduler.
        """
        print("\n" + "="*50)
        print(f"MasterAgent: Running trading loop iteration at {time.ctime()}")

        signal = self.signal_agent.generate_signal()
        ticker = self.strategy['asset_ticker']

        if signal == "BUY" and self.portfolio_manager.can_open_position(signal, ticker):
            print(f"MasterAgent: BUY signal received for {ticker}.")

            try:
                entry_price = self._get_current_price()
                stop_loss_price = self._calculate_stop_loss(entry_price)

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
                print(e)

        elif signal == "SELL":
            # For now, SELL signal is only used to close an existing long position.
            if ticker in self.portfolio_manager.positions:
                print(f"MasterAgent: SELL signal received for {ticker}. Closing position.")
                units_to_sell = self.portfolio_manager.positions[ticker]['units']
                self.broker.execute_order(ticker, "SELL", units_to_sell, reason="SIGNAL_EXIT")
            else:
                print("MasterAgent: SELL signal received, but no open position to close.")

        else: # HOLD
            print(f"MasterAgent: HOLD signal received for {ticker}. No action taken.")

        print("="*50 + "\n")

    def start(self, interval_seconds: int = 60):
        """
        Starts the autonomous trading loop.

        Args:
            interval_seconds (int): The time to wait between each trading loop iteration.
        """
        self.is_running = True
        print(f"HedgeFundMasterAgent started. Loop will run every {interval_seconds} seconds.")
        while self.is_running:
            self.run_trading_loop()
            time.sleep(interval_seconds)

    def stop(self):
        """Stops the trading loop."""
        print("HedgeFundMasterAgent stopping...")
        self.is_running = False
