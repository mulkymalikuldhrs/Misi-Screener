import os
import alpaca_trade_api as tradeapi
import pandas as pd
from typing import Optional
from utils.logger import logger

class AlpacaConnector:
    """
    A data connector for Alpaca to fetch real-time and historical market data.
    """

    def __init__(self, api_key: str = None, api_secret: str = None, base_url: str = None):
        """
        Initializes the Alpaca connector.
        """
        self.api_key = api_key or os.environ.get('ALPACA_API_KEY')
        self.api_secret = api_secret or os.environ.get('ALPACA_API_SECRET')
        # Note: Data API usually uses a different base URL for free vs pro, but REST client handles it.
        self.base_url = base_url or os.environ.get('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

        if not self.api_key or not self.api_secret:
            logger.warning("AlpacaConnector: API credentials not found.")
            self.api = None
        else:
            try:
                self.api = tradeapi.REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
            except Exception as e:
                logger.error(f"AlpacaConnector: Could not connect: {e}")
                self.api = None

    def get_historical_data(self, ticker: str, period: str = "1y", timeframe: str = "1Day") -> pd.DataFrame:
        """
        Fetches historical data from Alpaca.

        Args:
            ticker (str): The symbol to fetch.
            period (str): Simplified period (e.g., '1y', '1mo').
            timeframe (str): Alpaca timeframe (e.g., '1Min', '1Hour', '1Day').
        """
        if self.api is None:
            return pd.DataFrame()

        # Convert simplified period to start date
        from datetime import datetime, timedelta
        end_date = datetime.now()
        if period == '1y':
            start_date = end_date - timedelta(days=365)
        elif period == '1mo':
            start_date = end_date - timedelta(days=30)
        elif period == '1w':
            start_date = end_date - timedelta(days=7)
        elif period == '5d':
            start_date = end_date - timedelta(days=5)
        else:
            start_date = end_date - timedelta(days=365) # Default to 1y

        try:
            bars = self.api.get_bars(
                ticker,
                timeframe,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d')
            ).df

            if bars.empty:
                return pd.DataFrame()

            # Rename columns to match the system expectation (Title Case)
            bars = bars.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })

            # Ensure index is datetime and timezone-naive
            bars.index = pd.to_datetime(bars.index)
            if bars.index.tz is not None:
                bars.index = bars.index.tz_localize(None)

            return bars

        except Exception as e:
            logger.error(f"AlpacaConnector Error: {e}")
            return pd.DataFrame()
