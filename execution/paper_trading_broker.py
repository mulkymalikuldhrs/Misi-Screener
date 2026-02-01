from typing import Any

class PaperTradingBroker:
    """
    A simulated broker for paper trading. It simulates order execution with frictions.
    """

    def __init__(self, portfolio_manager: Any, data_connector: Any, slippage_percent: float = 0.05, commission_fee: float = 1.0):
        """
        Initializes the broker.

        Args:
            portfolio_manager (Any): An instance of PortfolioManager to record trades.
            data_connector (Any): An instance of a data connector to get current prices.
            slippage_percent (float): Simulated slippage as a percentage of the price.
            commission_fee (float): A flat fee charged per trade.
        """
        self.portfolio_manager = portfolio_manager
        self.data_connector = data_connector
        self.slippage_percent = slippage_percent
        self.commission_fee = commission_fee

    def get_current_price(self, ticker: str) -> float:
        """Fetches the most recent closing price for an asset."""
        data = self.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"PaperTradingBroker: Could not get current price for {ticker}.")
        return data['Close'].iloc[-1]

    def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY"):
        """
        Simulates the execution of a market order with slippage and commission.
        """
        if units <= 0:
            return

        try:
            base_price = self.get_current_price(ticker)

            # Apply slippage (price increases for BUY, decreases for SELL)
            slippage_factor = 1 + (self.slippage_percent / 100.0) if side == "BUY" else 1 - (self.slippage_percent / 100.0)
            execution_price = base_price * slippage_factor

            print(f"PaperTradingBroker: Executing {side} order for {units:.4f} {ticker} at ${execution_price:.2f} (slippage applied).")

            # Record the trade
            self.portfolio_manager.record_trade(
                ticker=ticker,
                side=side,
                units=units,
                price=execution_price,
                reason=reason
            )

            # Apply commission fee to cash balance
            self.portfolio_manager.cash -= self.commission_fee
            print(f"PaperTradingBroker: Applied commission fee of ${self.commission_fee:.2f}. New cash balance: ${self.portfolio_manager.cash:.2f}")

        except Exception as e:
            print(f"PaperTradingBroker Error: {e}")
