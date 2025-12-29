import yfinance as yf
import pandas as pd

class YFinanceConnector:
    """
    A connector to fetch market data using the yfinance library (Yahoo Finance API).
    """

    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetches historical OHLCV data for a given ticker.

        Args:
            ticker (str): The stock/crypto ticker symbol (e.g., "AAPL", "BTC-USD").
            period (str): The time period for the data (e.g., "1d", "1mo", "1y").

        Returns:
            pd.DataFrame: A DataFrame containing the historical data, with the index
                          as the date. Returns an empty DataFrame if the ticker is
                          not found or an error occurs.
        """
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period=period)

            if history.empty:
                print(f"Warning: No data found for ticker '{ticker}' for the period '{period}'.")
                return pd.DataFrame()

            # Convert timezone-aware index to timezone-naive
            if history.index.tz is not None:
                history.index = history.index.tz_localize(None)

            return history

        except Exception as e:
            print(f"An error occurred while fetching data for {ticker}: {e}")
            return pd.DataFrame()

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
