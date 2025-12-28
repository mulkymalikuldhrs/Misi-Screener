# TODO

This document tracks the planned future work for the MiSi Screener project.

## Next Up: High Priority

- [ ] **Implement the `Decision Support Layer` (`core/decision_support`):**
    -   Create the logic to synthesize the outputs from all core engines into a single, non-prescriptive summary.
- [ ] **Set up the basic `Data Pipeline` (`data/`):**
    -   Implement the initial data loaders and validators.
    -   Create the feature extraction logic to generate the inputs required by the core engines (e.g., ATR percentile, structure stability score).
- [ ] **Create the initial `FastAPI` endpoint (`api/fastapi`):**
    -   Build the first API endpoint to expose the output of the `Decision Support Layer`.

## Medium Priority

- [ ] **Design and build the initial `Frontend` charting interface (`frontend/charts`):**
    -   Visualize the outputs of the engines and the final decision support summary.
- [ ] **Add Logging and Monitoring:**
    -   Integrate a robust logging framework to track system behavior and decisions.
- [ ] **Refactor Engines for Performance:**
    -   Optimize the loops in the `MarketStructureEngine` and `LiquidityEngine` using vectorized operations for production performance.

## Low Priority

- [ ] Explore alternative data sources.
- [ ] Add more sophisticated feature engineering.
- [ ] Enhance the documentation with more detailed examples.

---

## Completed Tasks (v0.1.0)

-   ✅ **Implement the core logic for the `Market Structure Engine` (`core/structure`).**
-   ✅ **Implement the core logic for the `Liquidity & Participation Engine` (`core/liquidity`).**
-   ✅ **Implement the core logic for the `Regime Classification Engine` (`core/regime`).**
-   ✅ **Implement the core logic for the `Risk Governor` (`core/risk`).**
-   ✅ **Develop a comprehensive test suite for all core modules.**
