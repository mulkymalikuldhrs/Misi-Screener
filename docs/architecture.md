# MiSi Screener Architecture: A Multi-Agent AI Framework

## Core Concept: A Collaborative Team of AI Specialists

The MiSi Screener is architected as a multi-agent system, mirroring the structure of a sophisticated quantitative hedge fund. Each agent is a specialized AI with a distinct role. These agents collaborate, share insights, and debate conclusions to arrive at a holistic, data-driven trading decision.

---

### Architectural Flow

**1. Data Ingestion (`data_sources/`)**
   - The system begins by pulling in a massive volume of diverse data from multiple sources.
   - **Market Data:** Real-time and historical price/volume data (OHLCV).
   - **Fundamental Data:** Economic reports, company earnings, financial statements.
   - **Sentiment Data:** News feeds, social media APIs (e.g., X), geopolitical updates.

**2. The Analyst Team (`agents/`)**
   - This team of AI agents runs in parallel, each analyzing the incoming data from its own unique perspective.
   - **`TechnicalAnalystAgent`:** Processes price and volume data. It calculates hundreds of technical indicators (RSI, MACD, Bollinger Bands, etc.) and identifies market patterns and regimes.
   - **`FundamentalAnalystAgent`:** Parses economic reports and financial statements to assess the intrinsic value and health of assets.
   - **`SentimentAnalystAgent`:** Scans news and social media to gauge market sentiment, identifying trends of fear, greed, and hype.
   - **`GeopoliticalAnalystAgent`:** Monitors global events to assess their potential impact on market stability.

**3. The Strategy Library (`strategies/`)**
   - This directory contains a vast and ever-growing collection of hundreds of trading strategies.
   - Each strategy is a codified set of rules for entry, exit, and risk management (e.g., "RSI Mean Reversion," "Breakout on Volume Spike").
   - The AI will analyze this library to find the strategies that are best suited to the current market analysis.

**4. The Core Deciders (`agents/`)**
   - This is where the analysis is synthesized into an actionable decision.
   - **`TraderAgent`:** This is the central decision-making AI. It receives the reports from all Analyst agents. Its primary task is to "think hard"—to weigh the conflicting evidence, select the most appropriate strategy from the library, and generate a precise trade proposal, including entry price, position size, and risk parameters (stop-loss, take-profit).
   - **`RiskManagerAgent`:** This AI acts as the ultimate safety check. It receives the trade proposal from the `TraderAgent` and evaluates it against a set of portfolio-level risk constraints (e.g., max drawdown, correlation limits, exposure). It has the **absolute authority to veto any trade** that it deems too risky.

**5. Execution & Monitoring**
   - If a trade is approved by the `RiskManagerAgent`, the `TraderAgent` sends the order to the exchange.
   - The system then monitors the position, feeding real-time performance back into the `RiskManagerAgent`.

**6. The Dashboard (`dashboard/`)**
   - A real-time, intuitive web interface that provides a window into the AI's "mind."
   - It will visualize:
     - Key insights from each Analyst agent.
     - The strategy currently being considered or executed.
     - The final decision of the `TraderAgent` and the approval/veto from the `RiskManagerAgent`.
     - Real-time portfolio performance and risk metrics.

---

### Component Overview

-   **`main.py`:** The master orchestrator that initializes all agents and runs the main event loop.
-   **`agents/`:** Contains the individual AI agent classes, each with its own logic and prompts.
-   **`strategies/`:** A plug-and-play library of trading algorithms.
-   **`data_sources/`:** Modules for connecting to APIs and fetching data.
-   **`components/`:** Shared tools, such as the technical indicator library, risk calculators, and database connectors.
-   **`dashboard/`:** The frontend application for visualizing the system's operations.
