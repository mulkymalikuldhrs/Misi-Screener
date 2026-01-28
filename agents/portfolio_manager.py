import pandas as pd
from typing import Dict, Any, List

class PortfolioManager:
    """
    Manages the state of the trading portfolio, including cash, positions,
    and real-time valuation.
    """

    def __init__(self, initial_cash: float = 100000.0, data_connector: Any = None):
        """
        Initializes the portfolio.

        Args:
            initial_cash (float): The starting cash balance.
            data_connector (Any): A data connector to fetch live prices for valuation.
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {}  # Ticker -> { 'units': float, 'entry_price': float }
        self.trade_history: List[Dict[str, Any]] = []
        self.data_connector = data_connector

    def get_state(self) -> Dict[str, Any]:
        """
        Returns a snapshot of the current portfolio state, including unrealized P&L.
        """
        portfolio_value, positions_with_pnl = self._calculate_total_value()
        return {
            "cash": self.cash,
            "positions": positions_with_pnl,
            "portfolio_value": portfolio_value,
            "trade_count": len(self.trade_history)
        }

    def _calculate_total_value(self):
        """
        Calculates the total market value of the portfolio (cash + positions)
        using real-time market prices for open positions.
        """
        position_value = 0.0
        positions_with_pnl = self.positions.copy()

        if self.data_connector:
            for ticker, details in positions_with_pnl.items():
                try:
                    # Fetch the current market price
                    data = self.data_connector.get_historical_data(ticker, period="5d")
                    current_price = data['Close'].iloc[-1]
                    market_value = details['units'] * current_price

                    details['current_price'] = current_price
                    details['market_value'] = market_value
                    details['unrealized_pnl'] = market_value - (details['units'] * details['entry_price'])

                    position_value += market_value
                except Exception as e:
                    print(f"PortfolioManager: Could not fetch price for {ticker}. Valuing at cost. Error: {e}")
                    # If price fetch fails, value at entry price
                    position_value += details['units'] * details['entry_price']
        else:
            # Fallback for backtesting or when no connector is provided
            for ticker, details in self.positions.items():
                position_value += details['units'] * details['entry_price']

        return self.cash + position_value, positions_with_pnl

    def can_open_position(self, signal: str, ticker: str) -> bool:
        """
        Checks if a new position can be opened based on the signal.
        Prevents holding the same asset long while already long.
        """
        if signal == "BUY" and ticker in self.positions:
            print("PortfolioManager: Already holding a position. Cannot open another.")
            return False
        return True

    def calculate_position_size(self, risk_per_trade_percent: float, entry_price: float, stop_loss_price: float) -> float:
        """
        Calculates the number of units to buy for a new position based on portfolio risk.
        """
        total_value, _ = self._calculate_total_value()
        risk_amount_per_trade = total_value * (risk_per_trade_percent / 100.0)

        risk_per_unit = entry_price - stop_loss_price
        if risk_per_unit <= 0:
            return 0.0

        position_size_units = risk_amount_per_trade / risk_per_unit

        trade_cost = position_size_units * entry_price
        if trade_cost > self.cash:
            print("PortfolioManager: Not enough cash for desired position size. Sizing down.")
            position_size_units = self.cash / entry_price

        return position_size_units

    def record_trade(self, ticker: str, side: str, units: float, price: float, reason: str):
        """
        Updates the portfolio state after a trade is executed.
        """
        trade = {"ticker": ticker, "side": side, "units": units, "price": price, "reason": reason, "timestamp": pd.Timestamp.now()}
        self.trade_history.append(trade)

        if side == "BUY":
            self.cash -= units * price
            if ticker in self.positions:
                # Average down if position already exists
                total_cost = (self.positions[ticker]['units'] * self.positions[ticker]['entry_price']) + (units * price)
                total_units = self.positions[ticker]['units'] + units
                self.positions[ticker]['entry_price'] = total_cost / total_units
                self.positions[ticker]['units'] = total_units
            else:
                self.positions[ticker] = {'units': units, 'entry_price': price}

        elif side == "SELL":
            if ticker not in self.positions or units > self.positions[ticker]['units'] + 1e-9: # Epsilon for float
                print(f"PortfolioManager Warning: Attempting to sell more {ticker} than held.")
                return

            self.cash += units * price
            self.positions[ticker]['units'] -= units

            if self.positions[ticker]['units'] < 1e-9:
                del self.positions[ticker]

        print(f"PortfolioManager: Recorded {side} of {units:.4f} {ticker} @ ${price:.2f}. New cash: ${self.cash:.2f}")
