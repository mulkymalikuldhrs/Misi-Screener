# MiSi Screener Architecture: The Unified Vision

## Core Philosophy: A Modular Brain for a Dual-Purpose System

The architecture of MiSi Screener is designed around a central, powerful analytical "brain" that can be leveraged by two distinct operational branches. This allows the project to serve as both a fully autonomous trading agent and an interactive intelligence engine for human traders.

---

### At the Center: The 11 Intelligence Modules (`components/`)

This is the core of the entire system. It is a collection of 11 specialized, modular engines, each responsible for a different facet of institutional-grade market analysis. They are designed to be pure, reusable, and composable.

1.  **`macro_analysis`**: Analyzes global macro, geopolitics, and liquidity regimes.
2.  **`monetary_fundamental`**: Analyzes central bank policies, economic data, and asset fundamentals.
3.  **`positioning_crowd`**: Evaluates COT data, options positioning, and retail vs. institutional sentiment.
4.  **`intermarket`**: Analyzes cross-asset correlations and SMT divergences.
5.  **`market_structure`**: Performs deep SMC/ICT analysis on multiple timeframes.
6.  **`liquidity_orderflow`**: Maps liquidity pools and analyzes order flow narratives.
7.  **`order_book_venue`**: Analyzes the quality and risk of execution venues.
8.  **`dex_intelligence`**: Assesses risks specific to DEX tokens and new pairs.
9.  **`execution_plan`**: Synthesizes analysis into a concrete, multi-timeframe trade plan.
10. **`quant_scoring`**: Objectively scores the quality of a generated trade plan.
11. **`final_verdict`**: Produces the final, actionable output.

---

### Branch A: The Autonomous Agent Framework (`agents/`)

This branch uses the 11 intelligence modules to power a collective of autonomous AI agents that make and execute their own trading decisions.

-   **Workflow:**
    1.  **Analyst Agents** (e.g., `TechnicalAnalyst`, `FundamentalAnalyst`) use the relevant `components` modules to generate reports.
    2.  The **`TraderAgent`** receives these reports, uses the `ExecutionPlanBuilder`, `QuantScoringEngine`, and `FinalVerdictEngine` to form a final trade decision.
    3.  The decision is sent to the **`RiskManagerAgent`** for approval.
    4.  If approved, the trade is executed.
-   **Dashboard's Role:** In this mode, the dashboard acts as a **monitor**, providing a real-time view into the agents' activities and the portfolio's performance.

---

### Branch B: The Interactive Intelligence Framework (`dashboard/`)

This branch uses the 11 intelligence modules to serve a human trader via an interactive dashboard and chat interface.

-   **Workflow:**
    1.  A **human user** submits a query via the chat interface (e.g., "Generate a full report for BTC-USD").
    2.  The **FastAPI backend** (`dashboard/backend/`) receives the request.
    3.  The backend orchestrates a call to the **11 intelligence modules** to perform a complete analysis.
    4.  The final, synthesized report from the `FinalVerdictEngine` is formatted and sent back to the frontend.
-   **Dashboard's Role:** In this mode, the dashboard is an **interactive workspace**, allowing the user to request analyses, view detailed reports, and manage their own trading decisions based on the AI's institutional-grade insights.

---

This dual architecture allows for maximum flexibility. We can develop the core "brain" and have it immediately benefit both the autonomous and interactive sides of the project, creating a powerful, unified system for trading intelligence.
