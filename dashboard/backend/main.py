import asyncio
import os
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, Dict, List
import yaml

# Use absolute imports from the project root
from data_sources.yfinance_connector import YFinanceConnector
from data_sources.news_connector import NewsConnector
from data_sources.alpha_vantage_connector import AlphaVantageConnector
from agents.advanced_orchestrator import AIAgent
from agents.signal_agent import SignalAgent
from agents.portfolio_manager import PortfolioManager
from agents.risk_manager import RiskManager
from agents.technical_analyst import TechnicalAnalyst
from agents.master_agent import HedgeFundMasterAgent
from execution.paper_trading_broker import PaperTradingBroker

# --- Singleton State Manager ---
class HedgeFundStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HedgeFundStateManager, cls).__new__(cls)
            cls._instance.master_agent = None
            cls._instance.portfolio_manager = None
            cls._instance.agent_task = None
        return cls._instance

    def is_agent_running(self):
        return bool(self.master_agent and self.master_agent.is_running)

state_manager = HedgeFundStateManager()

# --- FastAPI App Initialization ---
app = FastAPI(
    title="MiSi Terminal API",
    description="API for the MiSi AI Quant Terminal & Hedge Fund.",
    version="4.0.0"
)

# --- Service Instantiation ---
yfinance_connector = YFinanceConnector()
news_connector = NewsConnector()
alpha_vantage_connector = AlphaVantageConnector()
technical_analyst = TechnicalAnalyst()

# --- API Models ---
class StartAgentRequest(BaseModel):
    strategy_filename: str

# --- API Endpoints ---

@app.post("/api/v1/agent/start")
async def start_agent(request: StartAgentRequest):
    """
    Initializes and starts the HedgeFundMasterAgent in a background asyncio task.
    The agent is now strategy-dynamic, loading based on the provided filename.
    """
    if state_manager.is_agent_running():
        raise HTTPException(status_code=400, detail="Agent is already running.")

    strategy_filepath = f"strategies/{request.strategy_filename}"
    if not os.path.exists(strategy_filepath):
        raise HTTPException(status_code=404, detail=f"Strategy file '{request.strategy_filename}' not found.")

    # Initialize all components for a trading session
    portfolio_manager = PortfolioManager(initial_cash=100000.0, data_connector=yfinance_connector)
    broker = PaperTradingBroker(portfolio_manager=portfolio_manager, data_connector=yfinance_connector)
    signal_agent = SignalAgent(strategy_filepath=strategy_filepath, data_connector=yfinance_connector)
    risk_manager = RiskManager(technical_analyst=technical_analyst, data_connector=yfinance_connector)

    master_agent = HedgeFundMasterAgent(
        signal_agent=signal_agent,
        portfolio_manager=portfolio_manager,
        risk_manager=risk_manager,
        broker=broker,
        strategy=signal_agent.strategy
    )

    state_manager.portfolio_manager = portfolio_manager
    state_manager.master_agent = master_agent

    # Run the agent's trading loop in a background asyncio task
    loop = asyncio.get_event_loop()
    state_manager.agent_task = loop.create_task(master_agent.start(interval_seconds=60))

    return {"status": "Hedge Fund Master Agent started successfully.", "strategy": signal_agent.strategy['strategy_name']}

@app.post("/api/v1/agent/stop")
async def stop_agent():
    """
    Stops the master agent's trading loop gracefully.
    """
    if not state_manager.is_agent_running():
        raise HTTPException(status_code=400, detail="Agent is not currently running.")

    state_manager.master_agent.stop()
    if state_manager.agent_task:
        state_manager.agent_task.cancel()
        state_manager.agent_task = None
    state_manager.master_agent = None

    return {"status": "Agent stopping. It will complete the current loop if active."}

@app.get("/api/v1/agent/status")
async def get_agent_status():
    """
    Returns the current running status of the master agent.
    """
    return {"is_running": state_manager.is_agent_running()}

@app.get("/api/v1/portfolio/state")
async def get_portfolio_state():
    """
    Retrieves the current state of the portfolio from the PortfolioManager.
    """
    if not state_manager.portfolio_manager:
        return {"status": "Portfolio not initialized. Start the agent first."}
    return state_manager.portfolio_manager.get_state()

@app.get("/api/v1/strategies")
async def list_strategies() -> List[Dict[str, Any]]:
    """
    Scans the /strategies directory and returns a list of available strategies.
    """
    strategies = []
    for filename in os.listdir("strategies"):
        if filename.endswith(".yml"):
            try:
                with open(f"strategies/{filename}", 'r') as f:
                    strategy_data = yaml.safe_load(f)
                    strategies.append({
                        "filename": filename,
                        "strategy_name": strategy_data.get("strategy_name", "N/A"),
                        "description": strategy_data.get("strategy_description", "No description.")
                    })
            except Exception as e:
                print(f"Could not load strategy {filename}: {e}")
    return strategies

# --- Static File Serving ---
app.mount("/static", StaticFiles(directory="dashboard/frontend"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serves the main index.html file."""
    return FileResponse('dashboard/frontend/index.html')
