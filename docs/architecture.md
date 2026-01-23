# System Architecture

The MiSi Screener platform has been architected as a modular, agent-based system designed for extensibility and realism. It separates concerns into distinct, specialized agents that collaborate to form a cohesive, autonomous trading engine. This document outlines the core components and their interactions.

## Core Principles

-   **Strategy-Agnostic Design**: The core engine is not hardcoded to any single trading strategy. New strategies can be defined in YAML files without requiring any changes to the underlying Python code.
-   **Delegation of Responsibility**: Each agent has a single, well-defined purpose (e.g., signal generation, risk management). This makes the system easier to maintain, test, and extend.
-   **Realism-First**: The components used in the backtester are the *exact same* components used in the live trading loop, ensuring that backtest performance is a reliable indicator of potential live performance.
-   **Asynchronous Operation**: The main trading loop runs in a non-blocking, asynchronous manner, allowing it to be managed by the web dashboard without halting the server.

## Component Breakdown

The system is composed of several key agents and managers that work in concert.

### 1. `HedgeFundMasterAgent`

-   **File**: `agents/hedge_fund_master_agent.py`
-   **Role**: The central orchestrator of the entire system. It does not contain any trading logic itself but is responsible for running the main trading loop and coordinating the actions of all other agents.
-   **Key Interactions**:
    -   Initializes and holds instances of all other agents.
    -   On each loop iteration, it queries the `SignalAgent` for a trading signal.
    -   If a "BUY" signal is received, it consults the `RiskManager` to determine the stop-loss and the `PortfolioManager` to calculate the position size.
    -   It then instructs the `Broker` to execute the trade.

### 2. `StrategyManager`

-   **File**: `agents/strategy_manager.py`
-   **Role**: To load, parse, and provide access to strategy configurations from YAML files located in the `strategies/` directory.
-   **Key Interactions**:
    -   It is initialized with a specific strategy file path.
    -   It provides the `HedgeFundMasterAgent` with easy access to strategy parameters, such as the asset ticker and risk management rules.

### 3. `SignalAgent`

-   **File**: `agents/signal_agent.py`
-   **Role**: To generate a discrete trading signal (`BUY`, `SELL`, or `HOLD`) based on the current market data and the loaded strategy's parameters.
-   **Key Interactions**:
    -   It receives the strategy configuration from the `StrategyManager`.
    -   It uses the `TechnicalAnalyst` to calculate the required technical indicators.
    -   It then applies the strategy's logic (e.g., RSI thresholds) to the indicator data to produce a final signal.

### 4. `TechnicalAnalyst`

-   **File**: `agents/technical_analyst.py`
-   **Role**: A facade for the technical indicator calculation library. It provides a clean, unified interface for other agents to access technical analysis.
-   **Key Interactions**:
    -   It uses the pure functions in `components/technical_indicators.py` to perform all calculations.
    -   It provides methods like `calculate_rsi` and `calculate_atr` that return raw data series for other agents to interpret.

### 5. `RiskManager`

-   **File**: `agents/risk_manager.py`
-   **Role**: To centralize all risk management logic. Its primary responsibility is to calculate stop-loss levels based on the strategy's rules.
-   **Key Interactions**:
    -   It is called by the `HedgeFundMasterAgent` *before* a trade is placed.
    -   It can calculate stop-losses using various methods, such as fixed-percentage or volatility-based (ATR).

### 6. `PortfolioManager`

-   **File**: `agents/portfolio_manager.py`
-   **Role**: To manage the state of the trading portfolio. It tracks cash, open positions, and trade history, and provides real-time valuation.
-   **Key Interactions**:
    -   It is used by the `HedgeFundMasterAgent` to calculate the appropriate position size for a new trade.
    -   It is updated by the `Broker` after every trade execution.
    -   It provides real-time P&L and portfolio value calculations by fetching live market data through its data connector.

### 7. `PaperTradingBroker` (Execution)

-   **File**: `execution/broker.py`
-   **Role**: To simulate the execution of trades. It mimics a real brokerage by handling order execution and notifying the `PortfolioManager` of trade fills.

## Data and Control Flow (Single Loop Iteration)

1.  The `HedgeFundMasterAgent`'s scheduled loop begins.
2.  `MasterAgent` -> `SignalAgent`: "Generate a signal."
3.  `SignalAgent` -> `DataConnector`: "Get me the latest market data for [ticker]."
4.  `SignalAgent` -> `TechnicalAnalyst`: "Calculate the RSI for this data."
5.  `SignalAgent` returns "BUY" to the `MasterAgent`.
6.  `MasterAgent` -> `PortfolioManager`: "Can we open a new position?"
7.  `MasterAgent` -> `RiskManager`: "Calculate the stop-loss for a trade on [ticker] at [entry_price]."
8.  `MasterAgent` -> `PortfolioManager`: "Calculate the position size based on this stop-loss."
9.  `MasterAgent` -> `Broker`: "Execute a BUY order for [X] units of [ticker]."
10. `Broker` executes the trade and calls -> `PortfolioManager`: "Record this trade."
11. The loop concludes and waits for the next scheduled iteration.
