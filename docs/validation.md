# Real Validation Framework

This document outlines the official, and only, sanctioned methods for validating the MiSi Screener system. Our validation philosophy is rooted in honesty, forward-looking observation, and a focus on failure analysis, not on simulated historical performance.

## Core Principle: No Backtesting

**Backtesting is strictly forbidden.**

Any attempt to validate the system's effectiveness using historical simulations ("backtests"), curve-fitting, or any form of performance optimization against past data is considered a violation of the project's core philosophy.

**Why is backtesting forbidden?**
1.  **Hindsight Bias:** Backtesting introduces perfect future knowledge, which is impossible in live conditions.
2.  **Curve-Fitting:** It encourages tweaking parameters to fit the past, creating a fragile system that is unlikely to perform well in the future.
3.  **Misleading Metrics:** Backtest reports (e.g., Sharpe ratio, equity curves) create a false sense of confidence and are fundamentally at odds with our non-predictive, risk-first approach.
4.  **Violation of Purpose:** The system's goal is to provide context, not to generate a profitable "strategy." Trying to measure its PnL is a misuse of the tool.

## Approved Validation Methods

### 1. Forward Observation

-   **Description:** The system is run on live, unseen market data in a read-only, "paper trading" mode.
-   **Process:**
    -   System outputs (regime classifications, risk alerts, etc.) are logged in real-time.
    -   These logs are periodically reviewed against the actual market behavior that occurred *after* the analysis was generated.
-   **Goal:** To assess whether the system's contextual analysis was helpful and accurate in real-time conditions, not whether it "would have made money."

### 2. Failure Case Logging

-   **Description:** This is the most critical validation method. We actively seek out, log, and analyze every instance where the system's output was wrong or misleading.
-   **Process:**
    -   A dedicated log (`failure_cases.log`) is maintained.
    -   Any time the system produces a demonstrably incorrect analysis (e.g., classifying a clear breakout as `Compression`), a detailed entry is made.
    -   Each entry must include the timestamp, the data that led to the error, the system's flawed output, and a hypothesis for the root cause.
-   **Goal:** To systematically identify and understand the system's weaknesses, leading to robust improvements.

### 3. Regime Mismatch Review

-   **Description:** A manual, qualitative review process where a human analyst periodically compares the system's regime classifications with their own discretionary assessment of the market.
-   **Process:**
    -   At the end of a session or week, the analyst reviews the charted regime labels produced by the system.
    -   They look for periods where the system's classification felt "wrong" or "out of sync" with the observed price action.
    -   These mismatches are documented and discussed to refine the regime engine's logic.
-   **Goal:** To ensure the system's context engine remains aligned with real-world market dynamics.

A system that is honest about its failures is infinitely more valuable than one that boasts of simulated successes.
