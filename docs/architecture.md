# System Architecture

The MiSi AI Hedge Fund platform is architected as a complete, end-to-end automated trading system. It is composed of several specialized, decoupled components that work in concert to find, execute, and manage trades.

```
Misi-Screener/
│
├── strategies/           # Definitive YAML files for trading strategies
├── agents/               # The "brains": core logic for signals, portfolio, and orchestration
├── execution/            # Simulated broker for paper trading
├── data_sources/         # Connectors for external data APIs
├── dashboard/            # The interactive web terminal for control and monitoring
├── tests/                # Unit and integration tests
└── run_backtest.py       # The standalone backtesting engine
```

### Core Trading Loop Components

The autonomous trading functionality is driven by a set of cooperative agents:

1.  **`SignalAgent` (`agents/signal_agent.py`)**
    -   **Role**: Strategy interpretation and signal generation.
    -   **Function**: Reads a strategy `.yml` file from the `strategies/` directory, calculates the necessary technical indicators (e.g., RSI) using real market data, and produces a discrete trading signal (`BUY`, `SELL`, or `HOLD`).

2.  **`PortfolioManager` (`agents/portfolio_manager.py`)**
    -   **Role**: The central state and risk management brain.
    -   **Function**: A stateful service that tracks the portfolio's cash balance, open positions, and trade history. Crucially, it is responsible for **position sizing**, ensuring that every trade adheres to the risk parameters defined in the strategy (e.g., risk 1% of the portfolio per trade).

3.  **`PaperTradingBroker` (`execution/paper_trading_broker.py`)**
    -   **Role**: Simulated trade execution.
    -   **Function**: Acts as a virtual broker. It takes an approved and sized order from the `PortfolioManager` and "executes" it at a simulated market price. It is designed to be extensible for future additions like slippage and commission modeling.

4.  **`HedgeFundMasterAgent` (`agents/master_agent.py`)**
    -   **Role**: The master orchestrator.
    -   **Function**: Runs the main autonomous **trading loop**. In each iteration, it:
        1.  Invokes the `SignalAgent` to get a new signal.
        2.  If a signal is generated, it consults the `PortfolioManager` to check for viability and calculate the correct position size.
        3.  If the trade is approved, it commands the `PaperTradingBroker` to execute the trade.
        4.  This loop is run in a background thread, allowing the system to trade autonomously.

### Control and Monitoring

-   **`dashboard/`**: The web terminal serves as the command center.
    -   The **FastAPI Backend** exposes endpoints (`/api/v1/agent/start`, `/api/v1/agent/stop`) that directly control the `HedgeFundMasterAgent`. It also provides an endpoint (`/api/v1/portfolio/state`) to query the `PortfolioManager` for real-time updates.
    -   The **Frontend UI** provides buttons to start and stop the agent and a `/portfolio` command to visualize the current state of the hedge fund.

### Strategy Validation

-   **`run_backtest.py`**: The "No Gimmick" Backtesting Engine.
    -   This is a standalone command-line script that provides a robust way to validate strategies before deployment.
    -   It uses the **exact same `SignalAgent`, `PortfolioManager`, and a slightly modified `BacktestingBroker`** to run a strategy over a historical dataset.
    -   By iterating through historical price data tick-by-tick and running the full agent logic at each step, it provides a realistic simulation of how a strategy would have performed, free of lookahead bias.
