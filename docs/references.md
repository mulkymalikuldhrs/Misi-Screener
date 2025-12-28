# References

This document lists the external, open-source references used to inform the concepts and architecture of MiSi Screener.

## Guiding Principles for Reference Integration

- **NO PLAGIARISM:** We do not copy-paste code or fork repositories directly. All implementations are reinterpretations and redesigns tailored to the MiSi Screener's production environment.
- **SYSTEM OVER NOTEBOOK:** Notebooks and research from references are treated as conceptual guides. The final output is always a modular, production-ready system.
- **AUDITABLE CONCEPTS:** Every concept integrated must be traceable to its source, with a clear understanding of its function and limitations.

## Primary Reference

- **Source:** [quant-science GitHub Organization](https://github.com/quant-science)
- **Date of Review:** 2023-10-27

### Concepts Adopted

The following concepts were identified as valuable and aligned with the MiSi Screener philosophy:

- **Regime-Aware Analysis:** The idea of classifying market behavior into distinct regimes (e.g., expansion, compression) is a core inspiration. This aligns with our non-predictive, context-first approach.
- **Volatility Measurement:** The use of robust volatility metrics (e.g., ATR-based, realized volatility) is adopted as a key input for regime classification and risk management.
- **Factor Hygiene:** The emphasis on clean, validated data and well-defined feature extraction pipelines informs our `data/` module design.

### Concepts Explicitly NOT Adopted

The following concepts and practices from the reference material were intentionally excluded:

- **Predictive Modeling:** Any models or components aimed at forecasting price direction or returns are rejected. This is in direct alignment with our non-predictive principle.
- **Backtest-Driven Claims:** We do not incorporate performance metrics or backtested results from the reference notebooks. MiSi Screener's value is in its real-time contextual analysis, not simulated historical performance.
- **Notebook-as-Product:** We explicitly avoid the practice of using research notebooks as final products. All logic is translated into robust, testable Python modules.

## Specific Implementations

### Market Structure Engine (`core/structure`)

-   **Reference:** First-Principles Design
-   **Justification:** During the research phase, direct inspection of code within potential reference repositories (like `quant-science`) was not possible due to technical limitations. To ensure the logic is 100% transparent, auditable, and deterministic, a "first-principles" approach was taken.
-   **Methodology:** The swing detection logic was built based on a simple, widely accepted, and non-ambiguous definition: a swing high is a candle with N lower highs on both sides, and a swing low is a candle with N higher lows on both sides.
-   **Advantages:** This approach guarantees zero reliance on black-box external code and aligns perfectly with the project's core value of auditability.

### Liquidity & Participation Engine (`core/liquidity`)

-   **Reference:** First-Principles Design
-   **Justification:** Similar to the Market Structure Engine, the inability to reliably inspect external codebases necessitated a first-principles approach to ensure auditability and determinism.
-   **Methodology:**
    -   **Participation Score:** Logic was developed based on the fundamental concepts of market participation, combining normalized volume and true range to create a dimensionless, percentile-ranked score. This avoids complex, opaque indicators.
    -   **Liquidity Sweeps:** The detection logic is based on a clear, observable market behavior: the failure of price to hold beyond a recent high or low. This is a purely mechanical definition that requires no predictive or probabilistic assumptions.
-   **Advantages:** The logic is 100% transparent, avoids dependency on broker-specific data (like order flow), and remains robust even in low-volume conditions.

### Regime Classification Engine (`core/regime`)

-   **Reference:** First-Principles Design, inspired by general quantitative finance concepts.
-   **Justification:** While the *idea* of regime classification was inspired by `quant-science`, the implementation is a pure, first-principles design to ensure it perfectly fits the MiSi Screener's architecture and philosophy.
-   **Methodology:**
    -   **Multi-Factor Input:** The engine synthesizes multiple, non-correlated factors (volatility, structure stability, participation) into a single, unified classification. This is a robust design pattern in quantitative systems.
    -   **Rule-Based Classifier:** A deterministic, rule-based classifier is used instead of a statistical or machine-learning model. This guarantees that the logic is 100% auditable, repeatable, and non-predictive. The rules are designed to map specific, observable market characteristics to the five official regimes.
-   **Advantages:** This approach avoids the "black box" problem of machine learning models and ensures that every regime classification can be explained and traced back to its root causes in the data.
