import yfinance as yf
import pandas as pd
from utils.logger import logger

class YFinanceConnector:
    """
    A connector to fetch market data using the yfinance library (Yahoo Finance API).

    yfinance returns columns with Title Case (e.g., 'Open', 'High', 'Low', 'Close', 'Volume').
    This connector normalizes column names to ensure consistency across the system.
    """

    # Canonical column names used throughout the system
    CANONICAL_COLUMNS = {'Open', 'High', 'Low', 'Close', 'Volume'}

    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetches historical OHLCV data for a given ticker.

        Args:
            ticker (str): The stock/crypto ticker symbol (e.g., "AAPL", "BTC-USD").
            period (str): The time period for the data (e.g., "1d", "1mo", "1y").

        Returns:
            pd.DataFrame: A DataFrame containing the historical data, with the index
                          as the date. Column names are normalized to Title Case
                          (Open, High, Low, Close, Volume). Returns an empty
                          DataFrame if the ticker is not found or an error occurs.
        """
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period=period)

            if history.empty:
                logger.warning(f"No data found for ticker '{ticker}' for the period '{period}'.")
                return pd.DataFrame()

            # Convert timezone-aware index to timezone-naive
            if history.index.tz is not None:
                history.index = history.index.tz_localize(None)

            # Normalize column names to Title Case to prevent KeyError
            # yfinance typically returns Title Case, but we ensure it defensively
            history.columns = self._normalize_columns(history.columns)

            return history

        except Exception as e:
            logger.error(f"An error occurred while fetching data for {ticker}: {e}")
            return pd.DataFrame()

    def _normalize_columns(self, columns) -> list:
        """
        Normalizes DataFrame column names to Title Case.
        Handles lowercase ('high'), uppercase ('HIGH'), and mixed case ('High').
        """
        normalized = []
        for col in columns:
            col_str = str(col)
            if col_str.lower() in {'open', 'high', 'low', 'close', 'volume'}:
                normalized.append(col_str.capitalize())
            else:
                normalized.append(col_str)
        return normalized

# Example usage:
if __name__ == '__main__':
    connector = YFinanceConnector()

    # Fetch Apple stock data for the last year
    aapl_data = connector.get_historical_data("AAPL", period="1y")
    if not aapl_data.empty:
        print("Successfully fetched AAPL data:")
        print(aapl_data.head())

    print("-" * 30)

    # Fetch Bitcoin data for the last month
    btc_data = connector.get_historical_data("BTC-USD", period="1mo")
    if not btc_data.empty:
        print("Successfully fetched BTC-USD data:")
        print(btc_data.head())
