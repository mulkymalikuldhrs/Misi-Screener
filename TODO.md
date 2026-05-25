# MiSi Screener AI - Project Roadmap (TODO)

This document tracks the development roadmap for the new, AI-driven MiSi Screener.

## Phase 1: Foundational AI Capabilities ✅

-   [X] **Pivot to AI-Centric Architecture:** Overhaul project to support a multi-agent framework.
-   [X] **Implement `TechnicalAnalystAgent` Skeleton:** Create the agent and the supporting `technical_indicators` component library.
-   [X] **Add Initial Indicators (ATR, RSI, MACD):** Implement and test the first set of core indicators.
-   [X] **Implement `FundamentalAnalystAgent`:** Built with real Alpha Vantage integration (PE ratio, earnings growth, etc.).
-   [X] **Implement `SentimentAnalystAgent`:** Built with real NewsAPI integration and keyword-based sentiment scoring.

## Phase 2: Core Decision-Making and Risk ✅

-   [X] **Implement `TraderAgent` Logic:** Synthesizes real signal/price data into trade proposals with risk/reward calculation.
-   [X] **Implement `RiskManager` Logic:** Full risk management with ATR stop-loss, evaluate_trade() validation, and configurable risk limits.
-   [X] **Build the Strategy Library:** YAML-based strategy definitions with `StrategyManager` for code-free strategy changes.
-   [X] **Create the `HedgeFundMasterAgent` Orchestrator:** Main loop that coordinates all agents, data flow, and decision-making with async architecture.

## Phase 3: Data and Execution ✅

-   [X] **Build `data_sources` Connectors:** Connectors for Yahoo Finance, Alpha Vantage, NewsAPI, and Alpaca.
-   [X] **Implement a Broker/Exchange Integration Layer:** Paper trading broker with slippage/commission simulation, plus Alpaca connector for live/paper trading.
-   [X] **SQLite Persistence:** Portfolio state, positions, and trade history persist across restarts via Peewee ORM.

## Phase 4: Dashboard and Visualization ✅

-   [X] **Build the Dashboard API:** FastAPI backend with modular endpoints for agent control, data queries, and AI orchestration.
-   [X] **Build the Terminal Frontend:** Interactive Bloomberg-style terminal with command palette, multi-panel layout, and chart visualization.

## Future Enhancements

-   [ ] **Advanced Technical Indicators:** Add Bollinger Bands, Stochastic Oscillator, Ichimoku Cloud, VWAP, etc.
-   [ ] **LLM-Powered Query Orchestrator:** Replace keyword-based parsing with a real language model for natural language queries.
-   [ ] **Advanced Risk Metrics:** Sharpe Ratio, Max Drawdown, Sortino Ratio in backtesting reports.
-   [ ] **Multi-Strategy Portfolio:** Support running multiple strategies simultaneously with cross-strategy risk management.
-   [ ] **Real-Time WebSocket Streaming:** Live price feeds and portfolio updates via WebSocket.
-   [ ] **Comprehensive Test Suite:** Expand test coverage across all agents, connectors, and risk management.

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
