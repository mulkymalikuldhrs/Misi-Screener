import os
import requests
import pandas as pd
from typing import Dict, Any
from utils.logger import logger

# IMPORTANT: To use this connector, you need a free Alpha Vantage API key.
# 1. Go to https://www.alphavantage.co/support/#api-key and claim your key.
# 2. Set the key as an environment variable named 'ALPHA_VANTAGE_API_KEY'.
#    For example, in your terminal: export ALPHA_VANTAGE_API_KEY='your_api_key_here'

class AlphaVantageConnector:
    """
    A connector to fetch fundamental financial data using the Alpha Vantage API.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        """
        Initializes the connector and retrieves the API key from environment variables.
        """
        self.api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            logger.warning("'ALPHA_VANTAGE_API_KEY' environment variable not found. AlphaVantageConnector will not work.")

    def _get_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Helper function to perform a GET request and handle basic errors."""
        if not self.api_key:
            return {"error": "API key is not configured."}

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raises an exception for bad status codes
            data = response.json()
            if "Error Message" in data:
                logger.error(f"Alpha Vantage API Error: {data['Error Message']}")
                return {}
            if "Information" in data: # Handles API call frequency limits
                logger.warning(f"Alpha Vantage API rate limit: {data['Information']}")
                return {}
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error occurred: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {}

    def get_company_overview(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches company overview data (market cap, P/E, etc.).

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            Dict[str, Any]: A dictionary containing the company overview.
        """
        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": self.api_key
        }
        return self._get_request(params)

    def get_income_statement(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches the annual income statement.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            Dict[str, Any]: A dictionary containing the annual reports.
        """
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": ticker,
            "apikey": self.api_key
        }
        return self._get_request(params)
