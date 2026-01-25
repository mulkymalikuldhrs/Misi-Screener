from typing import Dict, Any

class PaperTradingBroker:
    """
    A simulated broker for paper trading. It simulates order execution.
    """

    def __init__(self, portfolio_manager: Any, data_connector: Any):
        """
        Initializes the broker.

        Args:
            portfolio_manager (Any): An instance of PortfolioManager to record trades.
            data_connector (Any): An instance of a data connector to get current prices.
        """
        self.portfolio_manager = portfolio_manager
        self.data_connector = data_connector

    def _get_current_price(self, ticker: str) -> float:
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

    def execute_order(self, ticker: str, side: str, units: float, reason: str = "ENTRY", slippage_percent: float = 0.05, commission_fee: float = 1.00):
        """
        Simulates the execution of a market order with slippage and commission.

        Args:
            ticker (str): The asset to trade.
            side (str): 'BUY' or 'SELL'.
            units (float): The number of units to trade.
            reason (str): The reason for the trade.
            slippage_percent (float): The simulated price slippage in percent.
            commission_fee (float): The flat commission fee in dollars.
        """
        if units <= 0:
            print("PaperTradingBroker: Order for 0 units. No action taken.")
            return

        try:
            base_price = self._get_current_price(ticker)

            # --- Simulate Slippage ---
            if side == 'BUY':
                # Price is slightly higher for a buy
                execution_price = base_price * (1 + (slippage_percent / 100.0))
            else: # SELL
                # Price is slightly lower for a sell
                execution_price = base_price * (1 - (slippage_percent / 100.0))

            print(f"PaperTradingBroker: Base price for {ticker} is ${base_price:.2f}. After slippage, execution price is ${execution_price:.2f}.")

            # --- Simulate Commission ---
            # For simplicity, we'll deduct commission from the portfolio manager's cash
            # after the trade is recorded. A more complex simulation might adjust the
            # total cost of the trade itself.
            self.portfolio_manager.cash -= commission_fee
            print(f"PaperTradingBroker: Charged a ${commission_fee:.2f} commission.")

            print(f"PaperTradingBroker: Executing {side} order for {units:.4f} {ticker} at final price ${execution_price:.2f}.")

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
