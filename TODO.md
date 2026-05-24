# MiSi Screener AI - Project Roadmap (TODO)

This document tracks the development roadmap for the new, AI-driven MiSi Screener.

## Phase 1: Foundational AI Capabilities (In Progress)

-   [X] **Pivot to AI-Centric Architecture:** Overhaul project to support a multi-agent framework.
-   [X] **Implement `TechnicalAnalystAgent` Skeleton:** Create the agent and the supporting `technical_indicators` component library.
-   [X] **Add Initial Indicators (ATR, RSI, MACD):** Implement and test the first set of core indicators.
-   [ ] **Flesh out the `FeatureEngine`:** Add a comprehensive suite of indicators to `components/technical_indicators.py` (e.g., Bollinger Bands, Stochastic Oscillator, etc.).
-   [ ] **Implement `FundamentalAnalystAgent`:** Build the agent to ingest and analyze fundamental data (e.g., earnings reports, economic news).
-   [ ] **Implement `SentimentAnalystAgent`:** Build the agent to connect to news APIs and social media to gauge market sentiment.

## Phase 2: Core Decision-Making and Risk

-   [ ] **Implement `TraderAgent` Logic:** Develop the core "thinking" process where the agent synthesizes reports from the analyst team.
-   [ ] **Implement `RiskManagerAgent` Logic:** Build out the rules and logic for the risk agent to approve or veto trades based on portfolio-level constraints.
-   [ ] **Build the Strategy Library:** Add a diverse range of initial strategies to the `strategies/` directory that the `TraderAgent` can choose from.
-   [ ] **Create the `main.py` Orchestrator:** Implement the main loop that coordinates all agents, data flow, and decision-making.

## Phase 3: Data and Execution

-   [ ] **Build `data_sources` Connectors:** Create robust connectors for market data (e.g., Binance, Alpaca) and news APIs.
-   [ ] **Implement a Broker/Exchange Integration Layer:** Create the components needed to execute live or paper trades.

## Phase 4: Dashboard and Visualization

-   [ ] **Design the Frontend Dashboard:** Plan the UI/UX for visualizing the AI's analysis and the portfolio's performance.
-   [ ] **Build the Dashboard API:** Create the FastAPI backend to serve data to the frontend.
-   [ ] **Develop the Frontend Application:** Build the dashboard using a modern web framework.

## Ongoing Tasks

-   Continuously add more tests for all new components and agents.
-   Improve documentation.
-   Optimize performance.

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
