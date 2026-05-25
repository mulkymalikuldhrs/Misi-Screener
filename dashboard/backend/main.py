import asyncio
import os
from fastapi import FastAPI, HTTPException, Query, Body, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, Dict

# Use absolute imports
from data_sources.yfinance_connector import YFinanceConnector
from data_sources.news_connector import NewsConnector
from data_sources.alpha_vantage_connector import AlphaVantageConnector
from agents.advanced_orchestrator import AIAgent
from agents.signal_agent import SignalAgent
from agents.portfolio_manager import PortfolioManager
from agents.hedge_fund_master_agent import HedgeFundMasterAgent
from agents.strategy_manager import StrategyManager
from agents.risk_manager import RiskManager
from agents.technical_analyst import TechnicalAnalystAgent
from execution.paper_trading_broker import PaperTradingBroker

# --- Global State for the Hedge Fund ---
HEDGE_FUND_STATE: Dict[str, Any] = {
    "master_agent": None,
    "portfolio_manager": None,
}

# --- FastAPI App Initialization ---
app = FastAPI(
    title="MiSi Terminal API",
    description="API for the MiSi AI Quant Terminal & Hedge Fund.",
    version="2.0.0"
)

# --- Service Instantiation ---
yfinance_connector = YFinanceConnector()
news_connector = NewsConnector()
alpha_vantage_connector = AlphaVantageConnector()
technical_analyst = TechnicalAnalystAgent()

# --- Application Registry ---
APP_REGISTRY = {
    "get_historical_data": yfinance_connector.get_historical_data,
    "get_news_headlines": news_connector.get_headlines,
    "get_income_statement": alpha_vantage_connector.get_income_statement,
}

# Instantiate the main AI Agent with the app registry
ai_agent = AIAgent(APP_REGISTRY)

# --- API Endpoints ---

@app.post("/api/v1/agent/start")
async def start_agent():
    """
    Initializes and starts the HedgeFundMasterAgent.
    """
    if HEDGE_FUND_STATE.get("master_agent") and HEDGE_FUND_STATE["master_agent"]._is_running:
        raise HTTPException(status_code=400, detail="Agent is already running.")

    # Initialize all components
    strategy_filepath = "strategies/mean_reversion_rsi.yml"
    strategy_manager = StrategyManager(strategy_filepath=strategy_filepath)

    portfolio_manager = PortfolioManager(data_connector=yfinance_connector, initial_cash=100000.0)

    risk_manager = RiskManager(data_connector=yfinance_connector, technical_analyst=technical_analyst)

    signal_agent = SignalAgent(
        strategy_manager=strategy_manager,
        data_connector=yfinance_connector,
        technical_analyst=technical_analyst
    )

    broker = PaperTradingBroker(
        portfolio_manager=portfolio_manager,
        data_connector=yfinance_connector,
        slippage_percent=0.05,
        commission_fee=1.0
    )

    master_agent = HedgeFundMasterAgent(
        strategy_manager=strategy_manager,
        signal_agent=signal_agent,
        portfolio_manager=portfolio_manager,
        risk_manager=risk_manager,
        broker=broker
    )

    HEDGE_FUND_STATE["portfolio_manager"] = portfolio_manager
    HEDGE_FUND_STATE["master_agent"] = master_agent

    # Start the agent in the background
    master_agent.start(interval_seconds=60)

    return {"status": "Hedge Fund Master Agent started successfully."}

@app.post("/api/v1/agent/stop")
async def stop_agent():
    """
    Stops the master agent's trading loop.
    """
    master_agent = HEDGE_FUND_STATE.get("master_agent")
    if not master_agent or not master_agent._is_running:
        raise HTTPException(status_code=400, detail="Agent is not currently running.")

    master_agent.stop()
    return {"status": "Agent stopping."}

@app.get("/api/v1/portfolio/state")
async def get_portfolio_state():
    """
    Retrieves the current state of the portfolio.
    """
    portfolio_manager = HEDGE_FUND_STATE.get("portfolio_manager")
    if not portfolio_manager:
        return {"status": "Portfolio not initialized. Start the agent first."}

    return portfolio_manager.get_state()

# -- Terminal Application Endpoints --

class AIQuery(BaseModel):
    query: str

@app.post("/api/v1/ai-query")
async def handle_ai_query(request: AIQuery = Body(...)):
    """
    Handles a natural language query using the advanced AI Agent.
    """
    try:
        response = await ai_agent.handle_query(request.query)
        for result in response.get('results', []):
            if hasattr(result.get('data'), 'reset_index'):
                 result['data'] = result['data'].reset_index().to_dict(orient='records')
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/invoke/{app_name}")
async def invoke_app(app_name: str, ticker: str = Query(None), q: str = Query(None)) -> Any:
    """
    Invoke a data or analysis application directly.
    """
    if app_name not in APP_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Application '{app_name}' not found.")

    app_function = APP_REGISTRY[app_name]

    try:
        if app_name in ["get_historical_data", "get_income_statement"]:
            if not ticker:
                raise HTTPException(status_code=400, detail=f"The 'ticker' parameter is required for the '{app_name}' app.")
            data = app_function(ticker=ticker)
            if hasattr(data, 'reset_index'):
                return data.reset_index().to_dict(orient='records')
            return data
        elif app_name == "get_news_headlines":
            query = q or ticker
            if not query:
                raise HTTPException(status_code=400, detail="A 'q' or 'ticker' parameter is required.")
            return app_function(query=query)
        else:
            return app_function()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Static File Serving ---
# Resolve paths relative to this file to be robust
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    if not os.path.exists(INDEX_PATH):
        raise HTTPException(status_code=404, detail=f"Index file not found at {INDEX_PATH}")
    return FileResponse(INDEX_PATH)
