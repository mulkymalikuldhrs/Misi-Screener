from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any

# Use absolute imports, assuming the project root is in the PYTHONPATH
from data_sources.yfinance_connector import YFinanceConnector
from data_sources.news_connector import NewsConnector
from data_sources.alpha_vantage_connector import AlphaVantageConnector
from agents.query_orchestrator import QueryOrchestrator


# --- FastAPI App Initialization ---
app = FastAPI(
    title="MiSi Terminal API",
    description="API for the MiSi AI Quant Terminal.",
    version="2.0.0"
)

# --- Service Instantiation ---
# Instantiate our data connectors and the AI orchestrator.
yfinance_connector = YFinanceConnector()
news_connector = NewsConnector()
alpha_vantage_connector = AlphaVantageConnector()


# --- Application Registry ---
# This dictionary maps an "app_name" to a function that implements its logic.
APP_REGISTRY = {
    "get_historical_data": yfinance_connector.get_historical_data,
    "get_news_headlines": news_connector.get_headlines,
    "get_income_statement": alpha_vantage_connector.get_income_statement,
}

# Instantiate the AI orchestrator with the app registry
ai_orchestrator = QueryOrchestrator(APP_REGISTRY)


# --- API Endpoints ---
class AIQuery(BaseModel):
    query: str

@app.post("/api/v1/ai-query")
async def handle_ai_query(request: AIQuery = Body(...)):
    """
    Handles a natural language query by parsing it, calling the correct application,
    and returning the result.
    """
    app_name, params = ai_orchestrator.parse_query(request.query)

    if not app_name:
        raise HTTPException(status_code=400, detail="Could not understand the query. Please be more specific.")

    # Directly get the function from the registry
    app_function = APP_REGISTRY[app_name]

    try:
        # Perform parameter validation and call the function directly
        if app_name in ["get_historical_data", "get_income_statement"]:
            ticker = params.get('ticker')
            if not ticker:
                raise HTTPException(status_code=400, detail=f"The 'ticker' parameter is required for the '{app_name}' app.")
            data = app_function(ticker=ticker)
            if app_name == "get_historical_data":
                return {"app_name": app_name, "data": data.reset_index().to_dict(orient='records')}
            return {"app_name": app_name, "data": data}

        elif app_name == "get_news_headlines":
            query = params.get('q') or params.get('ticker')
            if not query:
                raise HTTPException(status_code=400, detail="A 'q' or 'ticker' parameter is required for the 'get_news_headlines' app.")
            data = app_function(query=query)
            return {"app_name": app_name, "data": data}

        else:
            data = app_function()
            return {"app_name": app_name, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while handling AI query: {str(e)}")


@app.get("/api/v1/invoke/{app_name}")
async def invoke_app(app_name: str, ticker: str = Query(None), q: str = Query(None)) -> Any:
    """
    Primary endpoint to invoke a data or analysis application directly.
    """
    if app_name not in APP_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Application '{app_name}' not found.")

    app_function = APP_REGISTRY[app_name]

    try:
        # Parameter validation remains here for direct invocations
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
