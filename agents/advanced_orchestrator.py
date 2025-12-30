import re
from typing import Dict, Any, List, Tuple, Optional

class AdvancedQueryOrchestrator:
    """
    An advanced orchestrator that can parse more complex natural language queries,
    including identifying multiple tickers.
    """

    def __init__(self):
        """
        Initializes the orchestrator's intent mapping.
        """
        self.intent_map = {
            "get_news_headlines": ["news", "headlines", "articles"],
            "get_income_statement": ["income", "revenue", "profit", "earnings", "fa"],
            "get_historical_data": ["price", "chart", "history"],
        }

    def _extract_tickers(self, query: str) -> List[str]:
        """
        Extracts all potential stock tickers (e.g., AAPL, MSFT, BTC-USD) from a query.
        """
        # This regex finds all uppercase words/phrases, including those with hyphens.
        return re.findall(r'\b[A-Z]{1,5}(?:-[A-Z]{1,5})?\b', query)

    def parse_query(self, query: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Parses a query to find a single intent and multiple entities (tickers).

        Args:
            query (str): The user's natural language query.

        Returns:
            A tuple containing the identified app_name and a dictionary of parameters.
            The 'tickers' parameter will be a list of strings.
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
        tickers = self._extract_tickers(query)
        if tickers:
            params['tickers'] = tickers

        return identified_app, params


class AIAgent:
    """
    The main AI agent that uses the orchestrator to process queries and call
    the necessary backend functions.
    """

    def __init__(self, app_registry: Dict[str, Any]):
        """
        Initializes the agent with an orchestrator and the app registry.
        """
        self.orchestrator = AdvancedQueryOrchestrator()
        self.app_registry = app_registry

    async def handle_query(self, query: str) -> Dict[str, Any]:
        """
        Handles a natural language query, orchestrates the necessary calls,
        and returns a structured response.

        Args:
            query (str): The user's natural language query.

        Returns:
            A dictionary containing the results, potentially from multiple API calls.
        """
        app_name, params = self.orchestrator.parse_query(query)

        if not app_name:
            raise ValueError("Could not understand the query. Please be more specific.")

        tickers = params.get('tickers')
        if not tickers:
            raise ValueError("No tickers found in the query.")

        # --- Execution Planning ---
        # For each ticker, call the identified application function.
        results = []
        app_function = self.app_registry.get(app_name)
        if not app_function:
            raise ValueError(f"Application '{app_name}' is not registered.")

        for ticker in tickers:
            try:
                # This part is simplified. A real implementation would use asyncio.gather
                # for concurrent API calls. For now, we call them sequentially.
                if app_name == "get_news_headlines":
                    result_data = app_function(query=ticker)
                else: # For /FA, /chart, etc.
                    result_data = app_function(ticker=ticker)

                # Append results in a structured way
                results.append({"ticker": ticker, "data": result_data})

            except Exception as e:
                results.append({"ticker": ticker, "error": str(e)})

        return {
            "query": query,
            "app_name": app_name,
            "results": results,
        }
