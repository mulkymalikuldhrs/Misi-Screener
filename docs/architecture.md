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
-   **Location:** `core/structure/engine.py`
-   **Function:** To objectively map the current market structure.
-   **Implementation Blueprint:** The engine is a stateless class that takes OHLC data and a lookback period as input. It identifies swing points based on a "first-principles" method.
-   **Inputs:**
    -   `ohlc_data`: A pandas DataFrame containing the price history.
    -   `lookback_period`: An integer `N` used to define the strength of a swing point.
-   **Outputs (`StructureOutput`):**
    -   `swing_points`: A list of `SwingPoint` objects, each containing the timestamp, price, type (High/Low), and strength of the detected swing.
-   **Core Logic (First Principles):**
    -   A **Swing High** is defined as a candle whose `high` is strictly greater than the `high` of the `N` preceding candles and the `N` succeeding candles.
    -   A **Swing Low** is defined as a candle whose `low` is strictly lower than the `low` of the `N` preceding candles and the `N` succeeding candles.
-   **Hard Prohibitions:** The logic is inherently non-repainting and uses a fixed lookback, ensuring that for a given dataset, the output is always identical.

### 1.2 Liquidity & Participation Engine
-   **Location:** `core/liquidity/engine.py`
-   **Function:** To measure market activity and pressure using a deterministic, first-principles approach.
-   **Implementation Blueprint:** A stateless class that takes OHLCV data and lookback periods as input.
-   **Inputs:**
    -   `ohlc_data`: A pandas DataFrame with columns including `high`, `low`, `close`, and `volume`.
    -   `participation_period`: The lookback window for normalizing the participation score.
    -   `sweep_lookback`: The lookback window for identifying recent highs/lows for sweep detection.
-   **Outputs (`LiquidityOutput`):**
    -   `participation_score`: A pandas Series providing a percentile-ranked score (0-100) for each candle, reflecting its combined volume and range activity relative to the lookback period.
    -   `liquidity_sweeps`: A list of `LiquiditySweep` events, marking specific points where a recent high/low was breached but the price failed to hold.
-   **Core Logic (First Principles):**
    -   **Participation Score:** Calculated by normalizing both volume and true range over the `participation_period` and combining them into a single score. This creates a robust measure of activity that is not dependent on absolute volume levels.
    -   **Liquidity Sweeps:** Detected by identifying when price pierces a high/low established within the `sweep_lookback` period, but the candle's close reverses back below/above that level, indicating a failure to continue.
-   **Design Mandate:** The logic is explicitly designed to avoid reliance on order flow or other broker-specific data, ensuring it is universally applicable and auditable.

---

## PHASE 2: REGIME ENGINE (The Heart of the System)

-   **Location:** `core/regime/engine.py`
-   **Function:** To classify the market's current behavioral state by synthesizing metrics from volatility, structure, and liquidity.
-   **Implementation Blueprint:** A stateless class that takes a `RegimeInput` data object and returns a `RegimeOutput` object. The core is a deterministic, rule-based classifier.
-   **Inputs (`RegimeInput`):**
    -   `atr_percentile`: A float (0.0-1.0) representing the percentile rank of the current ATR over a lookback period. This is the primary measure of **volatility**.
    -   `structure_stability`: A float (0.0-1.0) representing the clarity of the market's trend, derived from the `MarketStructureEngine`. This is the measure of **structure**.
    -   `participation_score`: A float (0-100) representing the intensity of market activity, taken from the `LiquidityEngine`. This is the measure of **liquidity**.
-   **Outputs (`RegimeOutput`):**
    -   `regime`: The classified `Regime` enum (e.g., `EXPANSION`, `COMPRESSION`).
    -   `confidence`: A score (0.0-1.0) indicating how well the inputs match the profile of the classified regime.
    -   `incompatible_actions`: A list of strings identifying trading logic that is invalid in the current regime.
-   **Core Logic (Rule-Based Classifier):**
    -   The engine uses a series of `if/elif` statements to check for specific combinations of the three inputs.
    -   **Stress / Breakdown:** Triggered by extremely high volatility and very low structure stability.
    -   **Compression:** Triggered by very low volatility and low participation.
    -   **Expansion:** Triggered by a combination of high volatility, high structure stability, and high participation.
    -   **Mean-Reversion:** Triggered by medium-to-high volatility but low structure stability (indicating chop).
    -   **Transition:** The default state if no other specific regime profile is met.
-   **Design Mandate:** The engine is explicitly not a predictive model. It is a descriptive classifier of the *current* market state based on observable, quantitative data.

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
