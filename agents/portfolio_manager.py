from typing import Dict, Any, List, Tuple

class PortfolioManager:
    """
    Manages the state of the trading portfolio, including cash, positions,
    and real-time valuation.
    """

    def __init__(self, data_connector: Any, initial_cash: float = 100000.0):
        """
        Initializes the portfolio.

        Args:
            data_connector (Any): An instance of a data connector for fetching live prices.
            initial_cash (float): The starting cash balance.
        """
        self.data_connector = data_connector
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.trade_history: List[Dict[str, Any]] = []

    def get_current_price(self, ticker: str) -> float:
        """Fetches the most recent price for a given ticker."""
        # Using a small period to get the latest available price
        data = self.data_connector.get_historical_data(ticker, period="5d")
        if data.empty:
            raise ValueError(f"PortfolioManager: Could not get current price for {ticker}.")
        return data['Close'].iloc[-1]

    def get_unrealized_pnl(self) -> Tuple[float, float]:
        """
        Calculates the unrealized profit and loss for all open positions.

        Returns:
            A tuple containing (total_pnl_absolute, total_pnl_percentage).
        """
        total_pnl = 0.0
        total_cost_basis = 0.0

        for ticker, details in self.positions.items():
            try:
                current_price = self.get_current_price(ticker)
                cost_basis = details['units'] * details['entry_price']
                market_value = details['units'] * current_price
                pnl = market_value - cost_basis
                total_pnl += pnl
                total_cost_basis += cost_basis
            except Exception as e:
                print(f"PortfolioManager Warning: Could not value position for {ticker}: {e}")
                # Fallback to cost basis (0 P&L)
                total_cost_basis += details['units'] * details['entry_price']

        pnl_percentage = (total_pnl / total_cost_basis) * 100 if total_cost_basis != 0 else 0.0
        return total_pnl, pnl_percentage

    def get_state(self) -> Dict[str, Any]:
        """Returns a snapshot of the current portfolio state with real-time valuation."""
        unrealized_pnl, _ = self.get_unrealized_pnl()
        return {
            "cash": self.cash,
            "positions": self.positions,
            "portfolio_value": self._calculate_total_value(),
            "unrealized_pnl": unrealized_pnl,
            "trade_count": len(self.trade_history)
        }

    def _calculate_total_value(self) -> float:
        """Calculates the total real-time market value of the portfolio."""
        position_value = 0.0
        for ticker, details in self.positions.items():
            try:
                current_price = self.get_current_price(ticker)
                position_value += details['units'] * current_price
            except Exception:
                # Fallback to entry price if live price is not available
                position_value += details['units'] * details['entry_price']
        return self.cash + position_value

    def can_open_position(self, signal: str, ticker: str) -> bool:
        """Checks if a new position can be opened."""
        if signal == "BUY" and ticker in self.positions:
            print("PortfolioManager: Already holding a position. Cannot open another.")
            return False
        return True

    def calculate_position_size(self, risk_per_trade_percent: float, entry_price: float, stop_loss_price: float) -> float:
        """Calculates the number of units to buy for a new position."""
        total_value = self._calculate_total_value()
        risk_amount_per_trade = total_value * (risk_per_trade_percent / 100.0)

        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit <= 0:
            return 0.0

        position_size_units = risk_amount_per_trade / risk_per_unit
        trade_cost = position_size_units * entry_price

        if trade_cost > self.cash:
            print("PortfolioManager: Not enough cash to open the desired position size. Sizing down.")
            position_size_units = self.cash / entry_price

        return position_size_units

    def record_trade(self, ticker: str, side: str, units: float, price: float, reason: str):
        """Updates the portfolio state after a trade is executed."""
        trade = {"ticker": ticker, "side": side, "units": units, "price": price, "reason": reason}
        self.trade_history.append(trade)

        if side == "BUY":
            self.cash -= units * price
            if ticker in self.positions:
                total_cost = (self.positions[ticker]['units'] * self.positions[ticker]['entry_price']) + (units * price)
                total_units = self.positions[ticker]['units'] + units
                self.positions[ticker]['entry_price'] = total_cost / total_units
                self.positions[ticker]['units'] = total_units
            else:
                self.positions[ticker] = {'units': units, 'entry_price': price}

        elif side == "SELL":
            if ticker not in self.positions:
                print(f"PortfolioManager Warning: Attempting to sell {ticker} which is not held.")
                return

            if units > self.positions[ticker]['units']:
                print(f"PortfolioManager Warning: Sizing down SELL order for {ticker} to match held units.")
                units = self.positions[ticker]['units']

            self.cash += units * price
            self.positions[ticker]['units'] -= units
            if self.positions[ticker]['units'] < 1e-9:
                del self.positions[ticker]

        print(f"PortfolioManager: Recorded {side} of {units:.4f} {ticker} @ ${price:.2f}. New cash balance: ${self.cash:.2f}")
