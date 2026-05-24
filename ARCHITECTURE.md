# Architecture Guide - MiSi Screener

> A detailed breakdown of the MiSi Screener system architecture, component interactions, data flow, and design decisions.

## Table of Contents

- [Executive Summary](#executive-summary)
- [Design Philosophy](#design-philosophy)
- [High-Level Architecture](#high-level-architecture)
- [Core Trading Loop](#core-trading-loop)
- [Agent Layer](#agent-layer)
- [Analytical Components](#analytical-components)
- [Data Layer](#data-layer)
- [Execution Layer](#execution-layer)
- [Dashboard & API Layer](#dashboard--api-layer)
- [Backtesting Engine](#backtesting-engine)
- [Data Flow Diagrams](#data-flow-diagrams)
- [Technology Stack](#technology-stack)
- [Security Considerations](#security-considerations)
- [Extensibility Guide](#extensibility-guide)

---

## Executive Summary

MiSi Screener is a quant-driven market intelligence platform architected as a multi-agent, event-driven system. It combines autonomous trading capabilities with an interactive intelligence terminal, enabling both hands-off strategy execution and hands-on market research. The platform operates on a philosophy of modularity and composability, where every analytical function is a discrete component that can be invoked independently or orchestrated by the AI agent to answer complex, multi-faceted questions.

The system is built around four foundational pillars: **Agent-Based Orchestration**, **Component-Driven Analysis**, **YAML Strategy Definition**, and **Reality-First Data Integration**. These pillars ensure that the platform remains extensible, testable, and grounded in real market data at every layer.

---

## Design Philosophy

The architecture follows the AI-first, sovereign-grade intelligence design philosophy established in the [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) ecosystem. Key architectural principles include:

1. **Separation of Concerns**: Each agent and component has a single, well-defined responsibility. The `SignalAgent` generates signals, the `PortfolioManager` manages risk, and the `HedgeFundMasterAgent` orchestrates them. This decoupling enables independent testing, modification, and replacement of any component.

2. **Strategy-as-Code via YAML**: Trading strategies are externalized into human-readable YAML configuration files rather than being hardcoded. This allows quantitative analysts to iterate on strategies without touching the Python codebase, while still leveraging the full power of the engine.

3. **Same-Component Testing**: The backtesting engine reuses the exact same `SignalAgent`, `PortfolioManager`, and broker components as the live trading system. This "no gimmick" approach ensures that backtested performance is a realistic proxy for live performance.

4. **Reality-First Data**: All analysis and trading decisions are grounded in real data from public APIs. There are no simulated or synthetic data feeds in the primary analysis pipeline. Simulated execution only occurs in the paper trading broker for risk-free strategy validation.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MiSi Screener Platform                       │
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐    │
│  │   Dashboard   │   │  Backtester  │   │  Strategy YAML   │    │
│  │   (Web UI)    │   │  (CLI Tool)  │   │  Definitions     │    │
│  └──────┬───────┘   └──────┬───────┘   └────────┬─────────┘    │
│         │                  │                     │               │
│  ┌──────┴──────────────────┴─────────────────────┴─────────┐    │
│  │                    Agent Layer                           │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │  Master Agent │  │  Signal Agent │  │  Portfolio   │  │    │
│  │  │  (Orchestrator)│  │  (Generator)  │  │  Manager     │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │  Technical   │  │ Fundamental  │  │  Sentiment   │  │    │
│  │  │  Analyst     │  │ Analyst      │  │ Analyst      │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  └────────────────────────┬─────────────────────────────────┘    │
│                           │                                      │
│  ┌────────────────────────┴─────────────────────────────────┐    │
│  │                 Component Layer                           │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐           │    │
│  │  │ Quant      │ │ Market     │ │ Liquidity  │           │    │
│  │  │ Scoring    │ │ Structure  │ │ Order Flow │           │    │
│  │  └────────────┘ └────────────┘ └────────────┘           │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐           │    │
│  │  │ Intermarket│ │ DEX        │ │ Final      │           │    │
│  │  │ Analysis   │ │ Intel      │ │ Verdict    │           │    │
│  │  └────────────┘ └────────────┘ └────────────┘           │    │
│  └────────────────────────┬─────────────────────────────────┘    │
│                           │                                      │
│  ┌────────────────────────┴─────────────────────────────────┐    │
│  │                  Data Layer                               │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐           │    │
│  │  │ Yahoo      │ │ Alpha      │ │ NewsAPI    │           │    │
│  │  │ Finance    │ │ Vantage    │ │ Connector  │           │    │
│  │  └────────────┘ └────────────┘ └────────────┘           │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                 Execution Layer                           │    │
│  │       Paper Trading Broker (Simulated Execution)         │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Trading Loop

The autonomous trading functionality is driven by the `HedgeFundMasterAgent`, which runs a continuous loop with the following lifecycle:

1. **Signal Generation**: The `SignalAgent` reads the active strategy YAML, calculates the required technical indicators using real market data from the `yfinance_connector`, and produces a discrete trading signal (`BUY`, `SELL`, or `HOLD`).

2. **Viability Check**: When a `BUY` signal is received, the `HedgeFundMasterAgent` consults the `PortfolioManager` to verify that the trade is viable given the current portfolio state, available capital, and risk constraints.

3. **Position Sizing**: The `PortfolioManager` calculates the appropriate position size based on the strategy's risk management parameters, specifically the `risk_per_trade_percent` and the distance between the entry price and the stop-loss price. This ensures consistent risk exposure across all trades.

4. **Order Execution**: If the trade is approved and sized correctly, the `HedgeFundMasterAgent` commands the `PaperTradingBroker` to execute the order. The broker simulates market execution at the current market price.

5. **Position Monitoring**: For open positions, the system monitors stop-loss levels. If a `SELL` signal is generated by the strategy, or if the stop-loss price is breached, the position is closed.

6. **Loop Iteration**: The entire cycle repeats at a configurable interval (default 60 seconds), allowing the system to continuously adapt to changing market conditions.

---

## Agent Layer

The agent layer is the decision-making core of the platform. Each agent is a Python class with a well-defined interface:

### HedgeFundMasterAgent (`agents/master_agent.py`)

The master orchestrator that coordinates all other agents. It maintains the trading loop state (`is_running`), manages the loop interval, and handles graceful start/stop operations. Key responsibilities include invoking the signal agent, consulting the portfolio manager for risk checks, calculating stop-loss levels, and commanding the broker to execute trades.

### SignalAgent (`agents/signal_agent.py`)

Responsible for strategy interpretation and signal generation. It reads a strategy YAML file from the `strategies/` directory, calculates the necessary technical indicators using real market data, and produces a discrete trading signal. The agent is stateless with respect to trading decisions, meaning it generates signals purely based on the current market state and strategy rules.

### PortfolioManager (`agents/portfolio_manager.py`)

The central state and risk management brain. It is a stateful service that tracks the portfolio's cash balance, open positions, and complete trade history. Its most critical function is **position sizing**, which ensures that every trade adheres to the risk parameters defined in the strategy. The position sizing algorithm uses the following formula:

```
position_size_units = (portfolio_value * risk_per_trade_percent / 100) / (entry_price - stop_loss_price)
```

This approach normalizes risk across all trades, regardless of the asset's price or volatility.

### AdvancedQueryOrchestrator (`agents/advanced_orchestrator.py`)

Parses natural language queries to identify user intent and extract relevant entities (stock tickers). It uses a keyword-based intent mapping system that can identify multiple tickers in a single query, enabling multi-asset analysis. The orchestrator routes parsed queries to the appropriate backend functions through the `APP_REGISTRY`.

### Specialized Analyst Agents

- **TechnicalAnalyst** (`agents/technical_analyst.py`): Performs technical analysis including pattern recognition, trend identification, and momentum assessment.
- **FundamentalAnalyst** (`agents/fundamental_analyst.py`): Conducts fundamental analysis including income statement evaluation, revenue analysis, and valuation metrics.
- **SentimentAnalyst** (`agents/sentiment_analyst.py`): Analyzes market sentiment from news headlines, social media signals, and general market tone.
- **RiskManager** (`agents/risk_manager.py`): Provides portfolio-level risk assessment including correlation analysis, concentration risk, and drawdown monitoring.
- **TraderAgent** (`agents/trader_agent.py`): Handles the mechanics of trade execution, order management, and fill tracking.

---

## Analytical Components

The component layer provides specialized analytical engines that feed into the agent layer:

### Quant Scoring Engine (`components/quant_scoring/`)

Aggregates signals from multiple analytical dimensions into a unified quantitative score. The engine applies weighted scoring across technical, fundamental, and sentiment indicators, producing a single composite score that represents the overall quality of a trading opportunity. Weights are configurable and can be adjusted per strategy.

### Final Verdict Engine (`components/final_verdict/`)

Takes the quant score and additional contextual factors (market regime, volatility environment, correlation structure) to produce a final verdict on each potential trade. The verdict includes a confidence level, a recommended action, and a list of supporting and opposing factors.

### Market Structure Engine (`components/market_structure/`)

Analyzes the structural characteristics of the market including trend state, volatility regime, and market phase identification. This component helps the agent layer understand whether the current market environment is conducive to the active strategy's assumptions.

### Liquidity & Order Flow Engine (`components/liquidity_orderflow/`)

Examines liquidity conditions and order flow patterns to assess market depth and potential slippage. This is particularly important for position sizing and execution timing.

### Order Book & Venue Engine (`components/order_book_venue/`)

Analyzes order book dynamics across venues to identify supply/demand imbalances and potential price impact.

### Intermarket Engine (`components/intermarket/`)

Evaluates correlations and relationships between different asset classes and markets. This component provides context on how macro relationships may affect the target asset.

### Positioning & Crowd Engine (`components/positioning_crowd/`)

Assesses crowd positioning and sentiment extremes. This contrarian indicator helps identify potential reversals when market participants are excessively positioned in one direction.

### DEX Intelligence Engine (`components/dex_intelligence/`)

Provides decentralized exchange analytics including liquidity pool analysis, token distribution, and on-chain metrics. This component bridges traditional market analysis with the emerging DeFi landscape.

### Macro Analysis Engine (`components/macro_analysis/`)

Evaluates macroeconomic indicators and their potential impact on market conditions. This includes analysis of GDP, inflation, employment, and other macroeconomic data releases.

### Monetary Fundamental Engine (`components/monetary_fundamental/`)

Analyzes monetary policy decisions, interest rate expectations, and central bank communications. This component provides context on the monetary environment in which trading decisions are made.

### Execution Plan Builder (`components/execution_plan/`)

Constructs detailed execution plans based on the trading signal, position size, and current market conditions. The builder considers factors such as order type, timing, and venue selection to optimize execution quality.

---

## Data Layer

The data layer provides a unified interface to external data sources through dedicated connector classes:

### YFinance Connector (`data_sources/yfinance_connector.py`)

Connects to Yahoo Finance via the `yfinance` library to fetch historical price data, current quotes, and market metadata. This is the primary data source for technical analysis and signal generation.

### Alpha Vantage Connector (`data_sources/alpha_vantage_connector.py`)

Connects to the Alpha Vantage API for fundamental data including income statements, balance sheets, and cash flow statements. This connector requires an API key set via the `ALPHA_VANTAGE_API_KEY` environment variable.

### News Connector (`data_sources/news_connector.py`)

Connects to the NewsAPI service to fetch news headlines and articles related to specific tickers or market topics. This connector requires an API key set via the `NEWS_API_KEY` environment variable.

All connectors follow a consistent interface pattern, making it straightforward to add new data sources without modifying the agent or component layers.

---

## Execution Layer

### Paper Trading Broker (`execution/paper_trading_broker.py`)

Acts as a virtual broker that simulates trade execution. It accepts orders from the `HedgeFundMasterAgent` and "executes" them at a simulated market price. The broker maintains a simple order book and trade log. It is designed with extensibility in mind for future additions such as slippage modeling, commission tracking, and partial fill simulation.

---

## Dashboard & API Layer

### FastAPI Backend (`dashboard/backend/main.py`)

The backend serves as the bridge between the agent layer and the web frontend. Key endpoints include:

- `POST /api/v1/agent/start` - Initialize and start the `HedgeFundMasterAgent`
- `POST /api/v1/agent/stop` - Gracefully stop the trading loop
- `GET /api/v1/portfolio/state` - Query the `PortfolioManager` for real-time portfolio state
- `POST /invoke/{app_name}` - Dynamic application invocation endpoint
- `POST /ai-query` - Natural language query processing via the orchestrator

### Web Frontend (`dashboard/frontend/index.html`)

A single-page application providing the interactive terminal interface. Features include a command palette (`Ctrl+K`), multi-panel layout, and real-time data visualization. The frontend communicates with the backend via REST API calls and renders data using vanilla JavaScript with optional charting libraries.

---

## Backtesting Engine

### `run_backtest.py` - The "No Gimmick" Backtester

The standalone backtesting engine provides robust strategy validation before live deployment. Key characteristics include:

- **Component Reuse**: Uses the exact same `SignalAgent` and `PortfolioManager` as the live system, with a slightly modified `BacktestingBroker` instead of the paper trading broker.
- **Tick-by-Tick Simulation**: Iterates through historical price data and runs the full agent logic at each time step, providing a realistic simulation of how a strategy would have performed.
- **No Lookahead Bias**: The backtester strictly processes data in chronological order, never accessing future data during signal generation or position management.
- **Performance Reporting**: Generates comprehensive performance reports including total return, maximum drawdown, Sharpe ratio, win rate, and individual trade history.

Usage:
```bash
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

---

## Data Flow Diagrams

### Autonomous Trading Flow

```
Strategy YAML ──► SignalAgent ──► Signal (BUY/SELL/HOLD)
                                       │
                                       ▼
                              HedgeFundMasterAgent
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼            ▼
                   PortfolioManager  Stop Loss   Current Price
                   (Viability +     Calculation   Fetch
                    Position Sizing)
                          │
                          ▼
                   PaperTradingBroker
                   (Execute Order)
                          │
                          ▼
                   Trade Log + Portfolio Update
```

### Interactive Query Flow

```
Natural Language Query ──► AdvancedQueryOrchestrator
                                    │
                           ┌────────┼────────┐
                           ▼        ▼        ▼
                       Intent    Entity    App
                       Detection  Extraction Registry Lookup
                           │        │        │
                           └────────┼────────┘
                                    ▼
                           Data Connector
                           (yfinance / Alpha Vantage / NewsAPI)
                                    │
                                    ▼
                           Structured Response
                           (Rendered in Dashboard)
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.11+ | Core application logic |
| Backend Framework | FastAPI + Uvicorn | REST API and WebSocket server |
| Data Processing | Pandas, NumPy | Market data manipulation and analysis |
| Technical Analysis | Custom (`components/technical_indicators.py`) | Indicator calculation |
| Strategy Definition | PyYAML | Human-readable strategy configuration |
| Data Sources | yfinance, NewsAPI, Alpha Vantage | Real-time and historical market data |
| Frontend | HTML/CSS/JavaScript | Interactive web terminal |
| Testing | pytest, pytest-asyncio | Unit and integration testing |
| Charting | TradingView Lightweight Charts | Price chart visualization |

---

## Security Considerations

- API keys are loaded from environment variables and are never hardcoded or committed to version control.
- The `.gitignore` file excludes `.env` files and other sensitive artifacts.
- The paper trading broker operates in simulation mode only. No real capital is at risk during strategy development and testing.
- All external API calls use HTTPS for encrypted data transmission.

---

## Extensibility Guide

### Adding a New Data Source Connector

1. Create a new Python file in `data_sources/` (e.g., `my_api_connector.py`).
2. Implement a connector class following the existing pattern (`yfinance_connector.py`, `news_connector.py`).
3. Load API keys from environment variables, never hardcode them.
4. Register the connector in the backend's `APP_REGISTRY` dictionary.
5. Add the corresponding command to the frontend's `APPS` array.
6. Implement the frontend renderer in the `renderSingleAsset` function.

### Adding a New Agent

1. Create a new agent class in `agents/` with a clear, single responsibility.
2. Define the agent's interface and integrate it with the `HedgeFundMasterAgent`'s orchestration logic.
3. Add unit tests in `tests/` for the new agent's core functionality.
4. Update the strategy YAML schema if the agent introduces new configurable parameters.

### Adding a New Component

1. Create a new directory in `components/` with an `engine.py` file.
2. Implement the analytical logic with clear input/output interfaces.
3. Integrate the component with the relevant agents that consume its output.
4. Add unit tests for the component's core calculations and edge cases.

---

## Related Projects

- [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) - The broader AI-native financial intelligence ecosystem
- [SolSniperX](https://github.com/mulkymalikuldhrs/SolSniperX) - AI-powered Solana memecoin sniper bot

## Author

**Mulky Malikul Dhaher**

- Email: mulkymalikuldhaher@email.com
- GitHub: [@mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)
