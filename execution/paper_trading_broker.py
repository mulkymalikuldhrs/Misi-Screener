import random
from typing import Any

class PaperTradingBroker:
    """
    A simulated broker for paper trading. It simulates order execution with
    realistic frictions like slippage and commission.
    """

    def __init__(self, portfolio_manager: Any, data_connector: Any, slippage_percent: float = 0.01, commission_fee: float = 0.50):
        """
        Initializes the broker.

        Args:
            portfolio_manager (Any): Instance of PortfolioManager to record trades.
            data_connector (Any): Instance of a data connector to get current prices.
            slippage_percent (float): Max slippage as a percentage (e.g., 0.01 for 0.01%).
            commission_fee (float): A flat commission fee per trade (e.g., $0.50).
        """
        self.portfolio_manager = portfolio_manager
        self.data_connector = data_connector
        self.slippage_percent = slippage_percent
        self.commission_fee = commission_fee

    def _get_current_price(self, ticker: str) -> float:
        """Fetches the most recent closing price for an asset."""
        data = self.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"Broker: Could not get current price for {ticker}.")
        return data['Close'].iloc[-1]

    def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY"):
        """
        Simulates the execution of a market order with slippage and commission.
        """
        if units <= 0:
            print("Broker: Order for 0 units. No action.")
            return

        try:
            base_price = self._get_current_price(ticker)

            # --- Simulate Slippage ---
            slippage = base_price * (self.slippage_percent / 100.0) * (random.random() - 0.5) * 2
            execution_price = base_price + slippage if side == "BUY" else base_price - slippage

            # --- Apply Commission ---
            # For simplicity, commission is deducted from cash in PortfolioManager after the trade
            # Here we just log it for transparency

            print(f"Broker: Executing {side} for {units:.4f} {ticker} at ~${base_price:.2f}")
            print(f"  -> Slippage adjusted price: ${execution_price:.2f}")
            print(f"  -> Commission: ${self.commission_fee:.2f}")

            # Record the trade with the portfolio manager
            self.portfolio_manager.record_trade(
                ticker=ticker,
                side=side,
                units=units,
                price=execution_price,
                reason=reason
            )
            # Deduct commission from cash
            self.portfolio_manager.cash -= self.commission_fee

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Broker: Unexpected error during order execution: {e}")
