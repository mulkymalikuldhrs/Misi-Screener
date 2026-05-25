from typing import Dict, Any, List, Optional
from utils.logger import logger


class SentimentAnalystAgent:
    """
    Analyzes news headlines, social media, and other text-based sources
    to gauge market sentiment.

    Status: Partially implemented — uses NewsAPI for headline sentiment
    when a news_api connector is available.
    """

    def __init__(self, news_api=None, social_media_api=None):
        self.news_api = news_api
        self.social_media_api = social_media_api

    def analyze(self, topic: str) -> Dict[str, Any]:
        """
        Takes in a topic (e.g., asset ticker or market sector) and produces a sentiment report.

        Args:
            topic: The topic to analyze.

        Returns:
            A dictionary summarizing the sentiment.
        """
        if not self.news_api and not self.social_media_api:
            return {
                "status": "not_configured",
                "message": "SentimentAnalyst: No news or social media API configured. "
                           "Provide a NewsConnector or social media data source to enable sentiment analysis.",
                "sentiment_score": None,
                "key_themes": [],
                "trending_narratives": [],
                "article_count": 0
            }

        try:
            articles = []
            if self.news_api:
                articles = self.news_api.get_headlines(query=topic, page_size=20)

            if not articles:
                return {
                    "status": "ok",
                    "message": f"No articles found for '{topic}'.",
                    "sentiment_score": 0.0,
                    "key_themes": [],
                    "trending_narratives": [],
                    "article_count": 0
                }

            # Simple keyword-based sentiment analysis
            positive_words = {'surge', 'rally', 'gain', 'profit', 'growth', 'bullish',
                              'upgrade', 'beat', 'exceed', 'soar', 'rise', 'record'}
            negative_words = {'crash', 'plunge', 'loss', 'decline', 'bearish', 'cut',
                              'miss', 'drop', 'fall', 'warning', 'risk', 'fear', 'sell'}

            pos_count = 0
            neg_count = 0
            themes = set()

            for article in articles:
                title = (article.get('title') or '').lower()
                description = (article.get('description') or '').lower()
                text = f"{title} {description}"

                has_pos = any(w in text for w in positive_words)
                has_neg = any(w in text for w in negative_words)

                if has_pos and not has_neg:
                    pos_count += 1
                elif has_neg and not has_pos:
                    neg_count += 1

                # Extract simple themes from title keywords
                for word in title.split():
                    word = word.strip('.,!?;:')
                    if len(word) > 4 and word.isalpha():
                        themes.add(word)

            total = pos_count + neg_count
            if total > 0:
                sentiment_score = (pos_count - neg_count) / total
            else:
                sentiment_score = 0.0

            return {
                "status": "ok",
                "sentiment_score": round(sentiment_score, 3),
                "key_themes": list(themes)[:10],
                "trending_narratives": [a.get('title', '') for a in articles[:5]],
                "article_count": len(articles)
            }

        except Exception as e:
            logger.error(f"SentimentAnalyst error analyzing '{topic}': {e}")
            return {
                "status": "error",
                "message": str(e),
                "sentiment_score": 0.0,
                "key_themes": [],
                "trending_narratives": [],
                "article_count": 0
            }
