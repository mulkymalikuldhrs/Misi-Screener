from typing import Dict, Any, Optional
from utils.logger import logger


class FundamentalAnalystAgent:
    """
    Analyzes economic data, company filings, and financial news to assess
    the intrinsic value of assets.

    Status: Partially implemented — uses Alpha Vantage for company overview
    when a data_source connector is available.
    """

    def __init__(self, data_source=None):
        self.data_source = data_source

    def analyze(self, asset: str) -> Dict[str, Any]:
        """
        Takes in an asset and produces a fundamental analysis report.

        Args:
            asset: The asset to analyze (e.g., a stock ticker).

        Returns:
            A dictionary summarizing the fundamental outlook.
        """
        if not self.data_source:
            return {
                "status": "not_configured",
                "message": "FundamentalAnalyst: No data source configured. "
                           "Provide an AlphaVantageConnector or similar to enable fundamental analysis.",
                "valuation": None,
                "growth_prospects": None,
                "economic_outlook": None,
                "red_flags": []
            }

        # Use the data source to fetch real fundamental data
        try:
            overview = self.data_source.get_company_overview(asset)
            if not overview or "error" in overview:
                return {
                    "status": "error",
                    "message": f"FundamentalAnalyst: Could not fetch data for {asset}.",
                    "valuation": None,
                    "growth_prospects": None,
                    "economic_outlook": None,
                    "red_flags": []
                }

            pe_ratio = overview.get('PERatio')
            pb_ratio = overview.get('PriceToBookRatio')
            peg_ratio = overview.get('PEGRatio')
            dividend_yield = overview.get('DividendYield')
            profit_margin = overview.get('ProfitMargin')
            earnings_growth = overview.get('QuarterlyEarningsGrowthYOY')

            # Determine valuation
            valuation = "Fair Value"
            if pe_ratio:
                pe = float(pe_ratio)
                if pe < 15:
                    valuation = "Undervalued"
                elif pe > 30:
                    valuation = "Overvalued"

            # Determine growth
            growth = "Stable"
            if earnings_growth:
                eg = float(earnings_growth)
                if eg > 0.15:
                    growth = "Strong Growth"
                elif eg < -0.05:
                    growth = "Declining"

            # Red flags
            red_flags = []
            if profit_margin and float(profit_margin) < 0:
                red_flags.append("Negative profit margin")
            if peg_ratio and float(peg_ratio) > 2:
                red_flags.append("High PEG ratio (>2)")

            return {
                "status": "ok",
                "valuation": valuation,
                "pe_ratio": pe_ratio,
                "pb_ratio": pb_ratio,
                "growth_prospects": growth,
                "earnings_growth": earnings_growth,
                "economic_outlook": "See macro analysis",
                "dividend_yield": dividend_yield,
                "profit_margin": profit_margin,
                "red_flags": red_flags
            }

        except Exception as e:
            logger.error(f"FundamentalAnalyst error analyzing {asset}: {e}")
            return {
                "status": "error",
                "message": str(e),
                "valuation": None,
                "growth_prospects": None,
                "economic_outlook": None,
                "red_flags": []
            }
