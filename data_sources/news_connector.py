import os
from newsapi import NewsApiClient
from typing import List, Dict, Any
from utils.logger import logger

# IMPORTANT: To use this connector, you need a NewsAPI key.
# 1. Go to https://newsapi.org/ and register for a free developer key.
# 2. Set the key as an environment variable named 'NEWS_API_KEY'.
#    For example, in your terminal: export NEWS_API_KEY='your_api_key_here'

class NewsConnector:
    """
    A connector to fetch real-time news headlines using the NewsAPI.
    """

    def __init__(self):
        """
        Initializes the NewsApiClient.

        It looks for the 'NEWS_API_KEY' environment variable.
        """
        try:
            # It's best practice to use environment variables for API keys.
            api_key = os.environ.get("NEWS_API_KEY")
            if not api_key:
                logger.warning("'NEWS_API_KEY' environment variable not found. NewsConnector will not be able to fetch articles.")
                self.api = None
            else:
                self.api = NewsApiClient(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize NewsApiClient: {e}")
            self.api = None

    def get_headlines(self, query: str, language: str = 'en', page_size: int = 20) -> List[Dict[str, Any]]:
        """
        Fetches top news headlines for a given query (e.g., a company name or ticker).

        Args:
            query (str): The search term (e.g., "Apple", "TSLA").
            language (str): The language of the articles (e.g., 'en', 'es').
            page_size (int): The number of results to return.

        Returns:
            List[Dict[str, Any]]: A list of articles, where each article is a dictionary.
                                  Returns an empty list if the API is not available or
                                  an error occurs.
        """
        if not self.api:
            return []

        try:
            top_headlines = self.api.get_everything(
                q=query,
                language=language,
                sort_by='publishedAt',
                page_size=page_size
            )

            if top_headlines['status'] == 'ok':
                return top_headlines['articles']
            else:
                logger.warning(f"Error from NewsAPI: {top_headlines.get('message', 'Unknown error')}")
                return []

        except Exception as e:
            logger.error(f"An error occurred while fetching news for '{query}': {e}")
            return []
