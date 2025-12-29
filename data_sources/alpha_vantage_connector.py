import os
import requests
import pandas as pd
from typing import Dict, Any

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
            print("Warning: 'ALPHA_VANTAGE_API_KEY' environment variable not found. AlphaVantageConnector will not work.")

    def _get_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Helper function to perform a GET request and handle basic errors."""
        if not self.api_key:
            return {"error": "API key is not configured."}

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raises an exception for bad status codes
            data = response.json()
            if "Error Message" in data:
                print(f"Alpha Vantage API Error: {data['Error Message']}")
                return {}
            if "Information" in data: # Handles API call frequency limits
                 print(f"Alpha Vantage API Info: {data['Information']}")
                 return {}
            return data
        except requests.exceptions.RequestException as e:
            print(f"An HTTP error occurred: {e}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
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

# Example usage:
if __name__ == '__main__':
    # Make sure you set your ALPHA_VANTAGE_API_KEY environment variable first.
    connector = AlphaVantageConnector()

    if connector.api_key:
        print("Fetching company overview for AAPL...")
        overview = connector.get_company_overview("AAPL")
        if overview:
            print(f"  Market Cap: {overview.get('MarketCapitalization')}")
            print(f"  P/E Ratio: {overview.get('PERatio')}")

        print("\n" + "-"*30 + "\n")

        print("Fetching income statement for AAPL...")
        income_statement = connector.get_income_statement("AAPL")
        if income_statement and 'annualReports' in income_statement:
            # Print the total revenue from the most recent annual report
            most_recent_report = income_statement['annualReports'][0]
            print(f"  Most Recent Fiscal Date: {most_recent_report.get('fiscalDateEnding')}")
            print(f"  Total Revenue: {most_recent_report.get('totalRevenue')}")
        else:
            print("Could not fetch or parse income statement.")
