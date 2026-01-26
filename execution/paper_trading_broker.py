from typing import Dict, Any
import random

class PaperTradingBroker:
    """
    A simulated broker for paper trading. It simulates order execution with realistic frictions.
    """

    def __init__(self, portfolio_manager: Any, data_connector: Any, slippage_percent: float = 0.01, commission_fee: float = 0.50):
        """
        Initializes the broker with configurable trading frictions.

        Args:
            portfolio_manager (Any): An instance of PortfolioManager to record trades.
            data_connector (Any): An instance of a data connector to get current prices.
            slippage_percent (float): The max percentage of slippage to apply.
            commission_fee (float): A fixed commission fee per trade.
        """
        self.portfolio_manager = portfolio_manager
        self.data_connector = data_connector
        self.slippage_percent = slippage_percent
        self.commission_fee = commission_fee

    def get_current_price(self, ticker: str) -> float:
        """
        Fetches the most recent closing price for an asset.

        NOTE: This is a simplification. A real-time system would use a streaming
        websocket API. For this simulation, we'll use the last available daily close.
        """
        # Fetch just the last few days to get the most recent price
        data = self.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"PaperTradingBroker: Could not get current price for {ticker}.")

        # Return the last known closing price
        return data['Close'].iloc[-1]

    def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY"):
        """
        Simulates the execution of a market order.

        In this simple version, we assume the order is filled instantly at the
        current market price without slippage or commission.

        Args:
            ticker (str): The asset to trade.
            side (str): 'BUY' or 'SELL'.
            units (float): The number of units to trade.
            reason (str): The reason for the trade (e.g., 'ENTRY', 'TAKE_PROFIT').
        """
        if units <= 0:
            print("PaperTradingBroker: Order for 0 units. No action taken.")
            return

        try:
            base_price = self.get_current_price(ticker)

            # Simulate slippage
            slippage = random.uniform(-self.slippage_percent, self.slippage_percent) / 100.0
            execution_price = base_price * (1 + slippage)

            # Deduct commission from portfolio
            self.portfolio_manager.cash -= self.commission_fee

            print(f"PaperTradingBroker: Executing {side} order for {units:.4f} {ticker} at simulated price ${execution_price:.2f} (includes slippage).")
            print(f"PaperTradingBroker: Commission of ${self.commission_fee:.2f} applied.")

            # Record the executed trade with the portfolio manager
            self.portfolio_manager.record_trade(
                ticker=ticker,
                side=side,
                units=units,
                price=execution_price,
                reason=reason
            )

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"PaperTradingBroker: An unexpected error occurred during order execution: {e}")
