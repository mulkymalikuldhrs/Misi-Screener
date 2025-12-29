# System Architecture

The MiSi Screener is designed as a modular, multi-component system to support its dual mission of autonomous operation and interactive analysis. The architecture is divided into several key directories at the project root.

```
Misi-Screener/
│
├── agents/               # Core AI logic and orchestration
├── data_sources/         # Connectors for external data APIs
├── dashboard/            # The interactive web terminal (frontend + backend)
│   ├── backend/
│   └── frontend/
├── components/           # (Future) Reusable, high-level analytical modules
└── tests/                # Unit and integration tests
```

### 1. Agents (`agents/`)

This is the "brain" of the system.
-   **`query_orchestrator.py`**: A foundational agent responsible for parsing natural language queries from the user. It uses intent recognition and entity extraction to map a query like *"Show me the latest news for AAPL"* to a specific, executable function call (e.g., `get_news_headlines(ticker='AAPL')`).
-   **(Future) Autonomous Agents**: This directory will house the logic for agents that can run independently, such as a `MarketScannerAgent` that continuously monitors for specific conditions or a `StrategyExecutionAgent` that manages trades.

### 2. Data Sources (`data_sources/`)

This directory follows the principles of a data abstraction layer, inspired by OpenBB. It contains all the code necessary to connect to and retrieve data from external, third-party APIs.
-   Each file is a **Connector** for a specific service (e.g., `yfinance_connector.py`, `alpha_vantage_connector.py`).
-   This approach decouples the rest of the system from the specifics of any single data provider. If an API changes or needs to be replaced, only the corresponding connector needs to be updated.

### 3. Dashboard (`dashboard/`)

This is the human-in-the-loop interface for the system—the interactive terminal.
-   **`frontend/`**: A single-page application built with vanilla HTML, CSS, and JavaScript. It implements a multi-panel, grid-based layout and a command palette (`Ctrl+K`) for invoking commands. It is a "thin client" that primarily renders data received from the backend.
-   **`backend/`**: A Python FastAPI server with two primary roles:
    1.  It serves the static `index.html` and its assets.
    2.  It exposes the API that the frontend and other system components use.

#### Key API Endpoints:
-   `GET /api/v1/invoke/{app_name}`: A direct, command-based endpoint that executes a specific analytical function (e.g., `get_income_statement`) from the `APP_REGISTRY`.
-   `POST /api/v1/ai-query`: The natural language endpoint. It takes a JSON object with a `query` string, passes it to the `QueryOrchestrator`, and then routes the resulting command to the `invoke` logic.

### 4. Components (`components/`)

This directory is reserved for higher-level, reusable analytical modules that are more complex than a simple data connector. Future examples might include:
-   A proprietary risk management model.
-   A complex technical analysis indicator library.
-   A portfolio construction and optimization engine.

These components can be called upon by agents or invoked directly through the terminal to perform their specific analysis.
