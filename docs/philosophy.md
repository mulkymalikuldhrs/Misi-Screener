# MiSi Screener Philosophy

## Core Principles (Non-Negotiable)

- **Non-predictive:** The system does not generate price targets or BUY/SELL signals. Its purpose is to provide context, not forecasts.
- **Risk-first:** All analytical modules are subordinate to the Risk Governor. Risk assessment precedes and overrides all other outputs.
- **Regime-aware:** Market context is prioritized over individual patterns or setups. The system's primary function is to classify the prevailing market regime.
- **Deterministic:** Given the same input data, the system will always produce the same output. There is no stochasticity or randomness in the core logic.
- **Audit-ready:** Every output can be traced back to its inputs and the specific logic that generated it. This ensures transparency and allows for rigorous verification.

## The Moral Contract: What MiSi Screener Will Never Do

This system operates under a strict set of self-imposed limitations. This is not a marketing statement; it is a technical and ethical contract.

1.  **It will never predict the future.** The system is forbidden from generating any output that could be misconstrued as a price forecast, target, or directional signal. Its purpose is to classify the *present*, not to guess the future.

2.  **It will never optimize for Profit & Loss (PnL).** The system's logic is not designed to maximize returns or any other performance metric. Its goal is to provide objective context and risk assessment, even if that context leads to fewer trading opportunities. The system's success is measured by the avoidance of fatal errors, not by the generation of profit.

3.  **It will never provide a "call to action".** The system will present its analysis (e.g., "Regime: Compression", "Risk: High"), but it will never suggest a specific action (e.g., "Buy now", "Target X"). The final decision and responsibility always rest with the user.

4.  **It will never operate on blind faith.** If the input data is deemed unreliable, incomplete, or noisy, the system is designed to halt its analysis and explicitly state "DATA NOT SUITABLE FOR ANALYSIS". It prefers silence over providing a potentially flawed assessment.

This philosophy ensures that MiSi Screener remains a tool for decision support, not a source of automated signals. A mature quantitative tool does not make you trade more often; it helps you make fewer fatal mistakes.
