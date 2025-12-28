# MiSi Screener

**MiSi Screener is a market intelligence system that helps traders not miss context, not helps them guess prices.**

This system is a non-predictive, regime-aware, and risk-first decision-support tool for financial market analysis. It is designed for production environments and emphasizes auditability and robustness over speculative forecasting.

## Core Philosophy

- **Non-Predictive:** We do not predict price. We classify market conditions.
- **Risk-First:** All analysis is governed by a master risk module.
- **Regime-Aware:** The central function is to identify the current market regime (e.g., Expansion, Compression).
- **Deterministic:** The same inputs always produce the same outputs.
- **Audit-Ready:** All outputs can be traced back to their source.

For a deeper dive into our principles, see [docs/philosophy.md](docs/philosophy.md).

## Architecture

The system is built on a modular architecture composed of a data pipeline, a core quant engine, and an API for delivering insights.

- **Data Pipeline:** Ingests, validates, and prepares market data.
- **Core Quant Engine:**
    - `Market Structure`: Identifies trends and structural points.
    - `Liquidity & Participation`: Measures market activity and pressure.
    - `Regime Classification`: Classifies the market regime.
    - `Risk Governor`: The master control for all system outputs.
    - `Decision Support`: Aggregates analysis into a clear summary.

For a detailed breakdown, see [docs/architecture.md](docs/architecture.md).

## Getting Started

> This section will be updated with installation and usage instructions.

## Limitations

This is not a predictive tool and does not guarantee any trading outcomes. It is a decision-support system that requires user discretion. For a full overview of the system's boundaries, please read [docs/limitations.md](docs/limitations.md).
