# References

This document lists the external, open-source references used to inform the concepts and architecture of the new, AI-driven MiSi Screener.

## Guiding Principles for Reference Integration

- **Inspiration, Not Imitation:** We analyze other projects to understand architectural patterns and potential features, but all implementations are designed from scratch to fit the unique vision of MiSi Screener.
- **Concept Over Code:** We are interested in the "what" and "why" of other systems, not the "how." We do not copy-paste code. The goal is to learn from the broader open-source community and build upon it.
- **Traceability:** Every major architectural decision or feature set inspired by an external source must be documented here with a clear justification.

---

## Key Inspirations for the AI-Agent Architecture

The current architecture of MiSi Screener is conceptually inspired by the following projects, which demonstrate a multi-agent approach to financial analysis.

-   **Sources:**
    -   `mulkymalikuldhrs/TradingAgents`
    -   `mulkymalikuldhrs/ai-agents-for-trading`
-   **Date of Review:** 2024-05-22

### Concepts Adopted

-   **Specialized Agent Roles:** The core architectural pattern of separating responsibilities into distinct agents (e.g., `TechnicalAnalyst`, `RiskManager`) is inspired by these repositories. This modular approach allows for greater specialization and scalability.
-   **Agent Collaboration Workflow:** The idea of having Analyst agents produce structured reports that are then synthesized by a final `TraderAgent` is a key workflow concept we have adapted.

### Concepts Explicitly REJECTED

-   **Specific LLM Prompts and Logic:** We do not use the proprietary prompts or the specific internal logic from these repositories. Our agents' "thinking" process will be developed independently.
-   **Direct Code Implementation:** No code from these repositories has been used. The inspiration is purely architectural.

---

## Feature Backlog Inspiration

While our implementation is from first principles, the following repository has proven useful as a "checklist" or "backlog" of standard, deterministic indicators to include in our `components` library.

-   **Source:** `mulkymalikuldhrs/quant-trading`

### Concepts Adopted

-   **"Universe of Indicators":** This repository provides an excellent list of common technical indicators (MACD, RSI, Bollinger Bands, ATR, etc.). We use this list to guide the development priorities for our `components/technical_indicators.py` library.

### Concepts Explicitly REJECTED

-   **Backtesting Framework:** The entire backtesting and signal-generation logic within the `quant-trading` scripts is explicitly rejected. In MiSi Screener, these indicators are used as **descriptive features for the AI**, not as prescriptive trading signals.

---
*Note: Previous references related to the deprecated, non-predictive version of this project have been removed to avoid confusion.*

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
