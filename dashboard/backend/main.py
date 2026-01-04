import threading
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
from agents.master_agent import HedgeFundMasterAgent
from execution.paper_trading_broker import PaperTradingBroker

# --- Global State for the Hedge Fund ---
# NOTE: In a production system, this state would be managed in a more robust
# way (e.g., a database, a dedicated state manager process). For this
# self-contained example, a global dictionary is sufficient.
HEDGE_FUND_STATE: Dict[str, Any] = {
    "master_agent": None,
    "portfolio_manager": None,
}

# --- FastAPI App Initialization ---
app = FastAPI(
    title="MiSi Terminal API",
    description="API for the MiSi AI Quant Terminal & Hedge Fund.",
    version="3.0.0"
)

# --- Service Instantiation ---
yfinance_connector = YFinanceConnector()
news_connector = NewsConnector()
alpha_vantage_connector = AlphaVantageConnector()

# --- Application Registry ---
APP_REGISTRY = {
    "get_historical_data": yfinance_connector.get_historical_data,
    "get_news_headlines": news_connector.get_headlines,
    "get_income_statement": alpha_vantage_connector.get_income_statement,
}

# Instantiate the main AI Agent with the app registry
ai_agent = AIAgent(APP_REGISTRY)

# --- API Endpoints ---

# -- Hedge Fund Control Endpoints --

@app.post("/api/v1/agent/start")
async def start_agent():
    """
    Initializes and starts the HedgeFundMasterAgent in a background thread.
    """
    if HEDGE_FUND_STATE.get("master_agent") and HEDGE_FUND_STATE["master_agent"].is_running:
        raise HTTPException(status_code=400, detail="Agent is already running.")

    # Initialize all components for a trading session
    portfolio_manager = PortfolioManager(initial_cash=100000.0)
    broker = PaperTradingBroker(portfolio_manager=portfolio_manager, data_connector=yfinance_connector)
    # For now, we hardcode the strategy. A future version could take this as a parameter.
    strategy_filepath = "strategies/mean_reversion_rsi.yml"
    signal_agent = SignalAgent(strategy_filepath=strategy_filepath, data_connector=yfinance_connector)

    master_agent = HedgeFundMasterAgent(
        signal_agent=signal_agent,
        portfolio_manager=portfolio_manager,
        broker=broker,
        strategy=signal_agent.strategy # Pass the loaded strategy dict
    )

    HEDGE_FUND_STATE["portfolio_manager"] = portfolio_manager
    HEDGE_FUND_STATE["master_agent"] = master_agent

    # Run the agent's trading loop in a separate thread to not block the API
    thread = threading.Thread(target=master_agent.start, args=(60,)) # Run loop every 60 seconds
    thread.daemon = True # Allows the main app to exit even if threads are running
    thread.start()

    return {"status": "Hedge Fund Master Agent started successfully."}

@app.post("/api/v1/agent/stop")
async def stop_agent():
    """
    Stops the master agent's trading loop.
    """
    master_agent = HEDGE_FUND_STATE.get("master_agent")
    if not master_agent or not master_agent.is_running:
        raise HTTPException(status_code=400, detail="Agent is not currently running.")

    master_agent.stop()
    HEDGE_FUND_STATE["master_agent"] = None # Clear the agent state
    return {"status": "Agent stopping. It will complete the current loop."}

@app.get("/api/v1/portfolio/state")
async def get_portfolio_state():
    """
    Retrieves the current state of the portfolio from the PortfolioManager.
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
    The agent parses the query, orchestrates calls, and returns a composite result.
    """
    try:
        # Delegate the entire query handling process to the AI agent
        response = await ai_agent.handle_query(request.query)
        # We need to manually process DataFrame outputs for JSON serialization
        for result in response.get('results', []):
            if hasattr(result.get('data'), 'reset_index'): # Check if it's a DataFrame
                 result['data'] = result['data'].reset_index().to_dict(orient='records')
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred in the AI agent: {str(e)}")


@app.get("/api/v1/invoke/{app_name}")
async def invoke_app(app_name: str, ticker: str = Query(None), q: str = Query(None)) -> Any:
    """
    Primary endpoint to invoke a data or analysis application directly.
    """
    if app_name not in APP_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Application '{app_name}' not found.")

    app_function = APP_REGISTRY[app_name]

    try:
        if app_name in ["get_historical_data", "get_income_statement"]:
            if not ticker:
                raise HTTPException(status_code=400, detail=f"The 'ticker' parameter is required for the '{app_name}' app.")
            data = app_function(ticker=ticker)
            if app_name == "get_historical_data":
                return data.reset_index().to_dict(orient='records')
            return data

        elif app_name == "get_news_headlines":
            query = q or ticker
            if not query:
                raise HTTPException(status_code=400, detail="A 'q' or 'ticker' parameter is required for the 'get_news_headlines' app.")
            return app_function(query=query)

        else:
            return app_function()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in '{app_name}': {str(e)}")


# --- Static File Serving ---
app.mount("/static", StaticFiles(directory="dashboard/frontend"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serves the main index.html file."""
    return FileResponse('dashboard/frontend/index.html')
