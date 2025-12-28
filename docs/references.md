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
