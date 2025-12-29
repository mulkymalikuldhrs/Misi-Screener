from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
import time
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Pydantic Models for API Response ---
class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float

class AnalysisReport(BaseModel):
    macro_context: str
    market_sentiment: str
    key_support_resistance: str
    market_structure: str
    smc_ict_analysis: str
    wave_analysis: str
    volume_profile: str
    candlestick_patterns: str
    intermarket_analysis: str
    statistical_indicators: str
    risk_assessment: str

class TechnicalDetails(BaseModel):
    rsi_14: float
    ma_20: float
    ma_50: float
    bollinger_upper: float
    bollinger_lower: float

class FullAnalysisResponse(BaseModel):
    asset: str
    chart_data: List[Candle]
    ai_analysis: AnalysisReport
    technical_details: TechnicalDetails

# --- FastAPI App Initialization ---
app = FastAPI(
    title="MiSi Screener API",
    description="API for the Sovereign Grade AI Quant Dashboard",
    version="1.0.0"
)

# --- Helper Functions for Data Generation ---
def generate_ohlcv_data(num_points=200):
    """Generates realistic-looking OHLCV data."""
    data = []
    price = 100
    timestamp = int(time.time()) * 1000  # Milliseconds
    for i in range(num_points):
        open_price = price + random.uniform(-1, 1)
        high_price = open_price + random.uniform(0, 2)
        low_price = open_price - random.uniform(0, 2)
        close_price = random.uniform(low_price, high_price)
        price = close_price

        # Ensure low is the lowest and high is the highest
        actual_low = min(open_price, close_price, low_price)
        actual_high = max(open_price, close_price, high_price)

        data.append({
            "time": timestamp - ((num_points - i -1) * 86400 * 1000), # Daily candles
            "open": round(open_price, 2),
            "high": round(actual_high, 2),
            "low": round(actual_low, 2),
            "close": round(close_price, 2)
        })
    return data

def generate_ai_analysis(asset: str) -> Dict[str, Any]:
    """Generates placeholder AI analysis text for all 11 modules."""
    return {
        "macro_context": f"Economic indicators suggest a period of consolidation for {asset}. Inflation concerns are currently priced in, but monetary policy shifts remain a key variable.",
        "market_sentiment": "Overall sentiment is neutral-to-bullish. Social media mentions are high, but institutional flows show a lack of strong conviction.",
        "key_support_resistance": "Major resistance is identified at the $52,000 level. Key support lies at the psychological $45,000 mark, coinciding with the 200-day moving average.",
        "market_structure": "The daily chart shows a potential higher low forming, indicating a possible continuation of the uptrend. A break below the previous swing low would invalidate this structure.",
        "smc_ict_analysis": "A significant Fair Value Gap (FVG) is present between $46,500 and $47,200, which may act as a magnet for price. Liquidity is resting above the recent highs.",
        "wave_analysis": f"The current price action for {asset} appears to be in a corrective Wave 4. We anticipate a final Wave 5 impulse to the upside, though the timing is uncertain.",
        "volume_profile": "The Point of Control (POC) for the last 90 days is at $48,000, indicating this as a major area of price agreement and potential support/resistance.",
        "candlestick_patterns": "A bullish engulfing candle was printed on the 3-day chart, suggesting a potential short-term reversal. However, confirmation on higher timeframes is needed.",
        "intermarket_analysis": f"The correlation between {asset} and the NASDAQ 100 remains high. Weakness in the tech sector could negatively impact {asset}'s price action.",
        "statistical_indicators": "Volatility has been contracting, as shown by the narrowing Bollinger Bands. This often precedes a significant price expansion.",
        "risk_assessment": "The current market regime is classified as 'low-volatility, trending'. Maximum drawdown risk is considered moderate. Position sizes should be adjusted accordingly."
    }

def generate_technical_details() -> Dict[str, Any]:
    """Generates placeholder technical indicator data."""
    rsi = round(random.uniform(40, 60), 2)
    ma_50 = round(random.uniform(48000, 49000), 2)
    ma_20 = ma_50 + round(random.uniform(-500, 500), 2)
    bollinger_upper = ma_20 + 400
    bollinger_lower = ma_20 - 400
    return {
        "rsi_14": rsi,
        "ma_20": ma_20,
        "ma_50": ma_50,
        "bollinger_upper": bollinger_upper,
        "bollinger_lower": bollinger_lower,
    }

# --- API Endpoints ---
@app.get("/api/v1/analysis", response_model=FullAnalysisResponse)
async def get_full_analysis(asset: str):
    """
    Provides a full, multi-faceted analysis for a given asset.
    This is the primary data endpoint for the dashboard.
    """
    if not asset:
        raise HTTPException(status_code=400, detail="Asset parameter is required.")

    # In a real application, you would fetch and process real data here based on the asset.
    # For this prototype, we generate placeholder data.
    chart_data = generate_ohlcv_data()
    ai_analysis = generate_ai_analysis(asset)
    tech_details = generate_technical_details()

    return {
        "asset": asset,
        "chart_data": chart_data,
        "ai_analysis": ai_analysis,
        "technical_details": tech_details,
    }

# --- Static File Serving ---
# Mount the static directory to serve frontend files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serves the main index.html file."""
    return FileResponse('../frontend/index.html')
