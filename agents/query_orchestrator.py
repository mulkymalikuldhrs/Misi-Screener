import re
from typing import Dict, Any, Tuple, Optional

class QueryOrchestrator:
    """
    A simple AI agent to parse natural language queries and map them to
    specific application calls.

    This is the foundational component for the AI-driven orchestration.
    In a real-world scenario, this would be replaced by a sophisticated
    NLP model (like a Large Language Model). For now, it uses simple
    keyword matching.
    """

    def __init__(self, app_registry: Dict[str, Any]):
        """
        Initializes the orchestrator with the available applications.

        Args:
            app_registry (Dict[str, Any]): A dictionary of the available apps,
                                           like the one in main.py.
        """
        self.app_registry = app_registry
        # Simple intent mapping using keywords.
        self.intent_map = {
            "get_news_headlines": ["news", "headlines", "articles"],
            "get_income_statement": ["income", "revenue", "profit", "earnings", "fa"],
            "get_historical_data": ["price", "chart", "history", "ohlc"],
        }

    def _extract_ticker(self, query: str) -> Optional[str]:
        """
        Extracts a stock ticker (usually an uppercase word) from the query.
        This is a simplified approach. A real system would use more robust
        Named Entity Recognition (NER).

        Args:
            query (str): The user's natural language query.

        Returns:
            Optional[str]: The extracted ticker, or None if not found.
        """
        # A simple regex to find uppercase words, which are often tickers.
        match = re.search(r'\b[A-Z]{1,5}\b', query)
        if match:
            return match.group(0)
        return None

    def parse_query(self, query: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Parses a natural language query to determine the target app and its parameters.

        Args:
            query (str): The user's natural language query.

        Returns:
            Tuple[Optional[str], Dict[str, Any]]: A tuple containing the identified
                                                  app_name and a dictionary of parameters
                                                  (e.g., {'ticker': 'AAPL'}).
                                                  Returns (None, {}) if no intent is found.
        """
        query_lower = query.lower()

        # 1. Intent Detection
        identified_app = None
        for app_name, keywords in self.intent_map.items():
            if any(keyword in query_lower for keyword in keywords):
                identified_app = app_name
                break

        if not identified_app:
            return None, {}

        # 2. Entity Extraction
        params = {}
        ticker = self._extract_ticker(query)
        if ticker:
            params['ticker'] = ticker
            # The query for news can also be the ticker itself
            params['q'] = ticker

        return identified_app, params

if __name__ == '__main__':
if __name__ == '__main__':
        # Example usage with a sample app registry
    example_registry = {
        "get_historical_data": None,
        "get_news_headlines": None,
        "get_income_statement": None,
    }

    orchestrator = QueryOrchestrator(example_registry)

    queries = [
        "show me the latest news for AAPL",
        "what was the revenue for MSFT last year?",
        "get me the price history for BTC-USD",
        "compare TSLA and F",
    ]

    for q in queries:
        app, params = orchestrator.parse_query(q)
        print(f"Query: '{q}'")
        if app:
            print(f"  -> App: '{app}', Params: {params}")
        else:
            print("  -> Could not determine intent.")
        print("-" * 20)
