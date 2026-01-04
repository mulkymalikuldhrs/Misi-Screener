from typing import Dict, Any, List

class PortfolioManager:
    """
    Manages the state of the trading portfolio, including cash, positions,
    and risk calculations.
    """

    def __init__(self, initial_cash: float = 100000.0):
        """
        Initializes the portfolio.

        Args:
            initial_cash (float): The starting cash balance.
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {} # Ticker -> { 'units': float, 'entry_price': float }
        self.trade_history: List[Dict[str, Any]] = []

    def get_state(self) -> Dict[str, Any]:
        """
        Returns a snapshot of the current portfolio state.

        TODO: Add unrealized P&L calculation based on current market prices.
        """
        return {
            "cash": self.cash,
            "positions": self.positions,
            "portfolio_value": self._calculate_total_value(),
            "trade_count": len(self.trade_history)
        }

    def _calculate_total_value(self) -> float:
        """
        Calculates the total market value of the portfolio (cash + positions).

        NOTE: This is a simplified version. A real implementation would need
        to fetch the current market price for each position to get its real-time value.
        For now, we'll value positions at their entry price.
        """
        position_value = 0.0
        for ticker, details in self.positions.items():
            position_value += details['units'] * details['entry_price']
        return self.cash + position_value

    def can_open_position(self, signal: str, ticker: str) -> bool:
        """
        Checks if a new position can be opened based on the signal.
        For this simple version, it just prevents holding the same asset long/short.
        """
        if signal == "BUY" and ticker in self.positions:
            print("PortfolioManager: Already holding a position. Cannot open another.")
            return False
        # Add logic for short selling if needed
        return True

    def calculate_position_size(self, risk_per_trade_percent: float, entry_price: float, stop_loss_price: float) -> float:
        """
        Calculates the number of units to buy for a new position.

        Args:
            risk_per_trade_percent (float): The percentage of total portfolio value to risk.
            entry_price (float): The price at which the trade will be entered.
            stop_loss_price (float): The price at which the trade will be exited for a loss.

        Returns:
            The number of units of the asset to purchase. Returns 0 if the trade is too risky.
        """
        total_value = self._calculate_total_value()
        risk_amount_per_trade = total_value * (risk_per_trade_percent / 100.0)

        risk_per_unit = entry_price - stop_loss_price
        if risk_per_unit <= 0:
            return 0.0

        position_size_units = risk_amount_per_trade / risk_per_unit

        # Check if we have enough cash
        trade_cost = position_size_units * entry_price
        if trade_cost > self.cash:
            print("PortfolioManager: Not enough cash to open the desired position size.")
            # We could resize the position to fit cash, but for now we'll just block it.
            return 0.0

        return position_size_units

    def record_trade(self, ticker: str, side: str, units: float, price: float, reason: str):
        """
        Updates the portfolio state after a trade is executed.

        Args:
            ticker (str): The asset ticker.
            side (str): 'BUY' or 'SELL'.
            units (float): The number of units traded.
            price (float): The execution price.
            reason (str): Reason for the trade (e.g., "ENTRY", "STOP_LOSS").
        """
        trade = {"ticker": ticker, "side": side, "units": units, "price": price, "reason": reason}
        self.trade_history.append(trade)

        if side == "BUY":
            self.cash -= units * price
            if ticker in self.positions:
                # Averaging down (not a typical strategy, but handle it)
                total_cost = (self.positions[ticker]['units'] * self.positions[ticker]['entry_price']) + (units * price)
                total_units = self.positions[ticker]['units'] + units
                self.positions[ticker]['entry_price'] = total_cost / total_units
                self.positions[ticker]['units'] = total_units
            else:
                self.positions[ticker] = {'units': units, 'entry_price': price}

        elif side == "SELL":
            if ticker not in self.positions or units > self.positions[ticker]['units']:
                print(f"PortfolioManager Warning: Attempting to sell more {ticker} than held.")
                return # Or raise an error

            self.cash += units * price
            self.positions[ticker]['units'] -= units

            # If all units are sold, remove the position
            if self.positions[ticker]['units'] < 1e-9: # Use a small epsilon for float comparison
                del self.positions[ticker]

        print(f"PortfolioManager: Recorded {side} of {units:.4f} {ticker} @ ${price:.2f}. New cash balance: ${self.cash:.2f}")
