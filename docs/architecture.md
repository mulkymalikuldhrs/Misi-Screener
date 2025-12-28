# MiSi Screener Architecture - Final Blueprint

## Definition of "Final"

A module or the system as a whole is considered "Final" only when it meets these criteria:
1.  It can be used effectively without any predictive capabilities.
2.  It remains useful and does not provide misleading information in adverse (choppy, low-volume) market conditions.
3.  It defaults to a "NO TRADE" or "NO CONTEXT" state more often than it identifies opportunities.
4.  Its logic can be easily audited and understood by a new engineer.
5.  It is robust enough that the failure of one non-critical module does not collapse the entire system.

---

## PHASE 1: CORE ENGINE (The Foundation)

The Core Engine consists of deterministic, non-predictive modules that analyze the raw price action.

### 1.1 Market Structure Engine
-   **Location:** `core/structure/`
-   **Function:** To objectively map the current market structure.
-   **Technical Deliverables:**
    -   `Swing Detector`: A deterministic algorithm to identify significant swing highs and lows.
    -   `BOS/CHoCH Flagger`: Flags Breaks of Structure (BOS) and Changes of Character (CHoCH) based on the swing map.
    -   `Structure Confidence Score`: A score indicating the clarity of the current structure (e.g., a clean trend vs. a choppy range), not a probabilistic forecast.
-   **Hard Prohibitions:** No repainting. No hindsight labeling. The output for a given candle must be final once the candle closes.

### 1.2 Liquidity & Participation Engine
-   **Location:** `core/liquidity/`
-   **Function:** To measure market activity and pressure.
-   **Technical Deliverables:**
    -   `Sweep Detection`: Identifies liquidity sweeps based on a combination of range expansion, volume, and session timing.
    -   `Participation Score`: A deterministic score (0-100) reflecting the intensity of market participation.
-   **Design Mandate:** Must be robust enough to function in low-volume environments and not be dependent on a specific broker's data feed.

---

## PHASE 2: REGIME ENGINE (The Heart of the System)

-   **Location:** `core/regime/`
-   **Function:** To classify the market's current behavioral state. This is the central context engine.
-   **Finalized Regimes:**
    -   `Expansion`: Characterized by increasing volatility and directional movement.
    -   `Compression`: Characterized by decreasing volatility and range contraction.
    -   `Transition`: The state between Expansion and Compression.
    -   `Mean-reversion`: Conditions favoring a return to a statistical mean.
    -   `Stress / Breakdown`: Highly volatile, unpredictable conditions often associated with major news events or structural failures.
-   **Inputs:**
    -   Volatility behavior (realized vol, ATR-relative metrics).
    -   Structure stability score from the Structure Engine.
    -   Liquidity behavior from the Liquidity Engine.
-   **Outputs:**
    -   `Regime Label`: The current classified regime.
    -   `Regime Confidence`: A score of how clearly the data fits the regime profile.
    -   `Incompatible Actions`: A list of trading logic types that are invalid in the current regime (e.g., "Breakout logic invalid" during `Compression`).

---

## PHASE 3: RISK GOVERNOR (The Ultimate Authority)

-   **Location:** `core/risk/governor.py`
-   **Function:** To act as the master control switch for the entire system. Its directives are absolute and cannot be overridden by the user.
-   **Implementation Blueprint:** The governor is implemented as a stateless class that takes a `RiskInput` data object and returns a `GovernorDirective` object. The logic is a cascading series of rules, ensuring that the most critical risk factors are checked first.
-   **Inputs (`RiskInput`):**
    -   `realized_volatility` & `volatility_percentile`: To measure current market volatility against historical norms.
    -   `current_regime` & `regime_confidence`: To understand the market context provided by the Regime Engine.
    -   `system_drawdown` & `is_new_equity_high`: To assess the current performance and risk exposure.
    -   `data_integrity_score`: To ensure the quality of the data underpinning the analysis.
-   **Outputs (`GovernorDirective`):**
    -   `permission_state`: The final, non-negotiable state (`ALLOW`, `RESTRICT`, `BLOCK`).
    -   `reason`: A human-readable explanation for the current state.
-   **Core Logic (Cascading Rules):**
    1.  **Data Integrity Failure?** → `BLOCK`
    2.  **Market Regime is "Stress"?** → `BLOCK`
    3.  **Volatility in >95th Percentile?** → `BLOCK`
    4.  **System Drawdown > 20%?** → `BLOCK`
    5.  **High Volatility + System Drawdown?** → `RESTRICT`
    6.  **Low Regime Confidence?** → `RESTRICT`
    7.  **Otherwise** → `ALLOW`
-   **Gate:** The system is considered mature only when this logic results in a `BLOCK` or `RESTRICT` state for the majority of the time.

---

## PHASE 4: DECISION SUPPORT LAYER (The Anti-Signal Interface)

-   **Location:** `core/decision_support/`
-   **Function:** To translate the complex outputs of the core engines into a simple, non-actionable summary for the user.
-   **Displayed Information:**
    -   Market State Summary (e.g., "Trending Up, High Confidence")
    -   Regime Badge (e.g., "COMPRESSION")
    -   Risk Status (e.g., "HIGH - RESTRICTED")
    -   Setup Compatibility (e.g., "Mean-Reversion Setup: YES")
-   **Forbidden Information:** Entry prices, Take Profit/Stop Loss levels, forecasts.

---

## PHASE 5: DATA & NOISE DEFENSE

-   **Location:** `data/`
-   **Function:** To ensure the system operates only on high-quality data and refuses to analyze garbage.
-   **Key Components:**
    -   `Data Integrity Score`: A metric to score the quality of the incoming data stream.
    -   `Explicit Missing Data Handling`: Clear logic for how gaps in data are handled (e.g., halt analysis, never fill).
    -   `Latency Awareness`: The system must be aware of potential data latency and flag it.
-   **Core Principle:** It is better to refuse analysis than to provide a flawed one.

---

## PHASE 6: API & FRONTEND (Minimalist & Honest)

-   **Locations:** `api/`, `frontend/`
-   **Design Philosophy:** The UI/UX must not encourage over-trading or create emotional responses.
-   **UI Principles:**
    -   Use a neutral color palette. Avoid excessive use of "profit green" or "loss red".
    -   Warnings and error states should be more prominent than "success" states.
-   **API Principles:**
    -   Must be stateless.
    -   Responses must be deterministic.
    -   Outputs must be versioned to ensure long-term stability.

---

## PHASE 7: REAL VALIDATION (Not Backtesting)

-   **Location:** `docs/validation.md`
-   **Function:** To define a rigorous, honest process for validating the system's effectiveness.
-   **Approved Validation Methods:**
    -   `Forward Observation`: Analyzing system performance on live, unseen data.
    -   `Failure Case Logging`: Actively logging and reviewing every instance where the system's analysis was incorrect or misleading.
    -   `Regime Mismatch Review`: Manually reviewing periods where the classified regime did not match reality.
-   **Forbidden Validation Methods:** Backtesting, curve-fitting, "what-if" scenarios, or any claims of historical performance.

---

## PHASE 8: OPEN SOURCE HYGIENE

-   **Required Documents:** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
-   **`docs/references.md` Mandate:** This file must be maintained with explicit details on what concepts were adopted from external sources (like `quant-science`), why they were chosen, and how they were modified to fit the MiSi Screener philosophy.
