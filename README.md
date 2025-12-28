# MiSi Screener

**MiSi Screener is a market intelligence system that helps traders avoid the wrong context and fatal risks — without predictions, without signals.**

This system is a non-predictive, regime-aware, and risk-first decision-support tool for financial market analysis. It is designed for production environments and emphasizes auditability, determinism, and robustness over speculative forecasting.

## Core Philosophy

The entire system is built on a set of non-negotiable principles:

-   **Non-Predictive:** We do not predict price. We classify market conditions.
-   **Risk-First:** All analysis is governed by the `RiskGovernor`, whose directives are absolute.
-   **Regime-Aware:** The central function is to identify the current market regime (e.g., `Expansion`, `Compression`).
-   **Deterministic:** The same inputs will always produce the same outputs.
-   **Audit-Ready:** All logic is transparent and traceable.

For a deeper dive into our principles, see **[docs/philosophy.md](docs/philosophy.md)**.

## Architecture

The system is a modular, layered application designed for clarity and robustness.

1.  **Data Pipeline:** Ingests, validates, and prepares market data with a strict "garbage in, halt analysis" policy.
2.  **Core Quant Engine:** A series of deterministic modules that analyze market data:
    -   `Market Structure Engine`: Objectively maps market structure (swing points, BOS/CHoCH).
    -   `Liquidity & Participation Engine`: Measures market activity and pressure.
    -   `Regime Classification Engine`: The heart of the system; classifies the market's behavioral state.
    -   `Risk Governor`: The ultimate authority. It assesses systemic risk and has the power to **BLOCK** or **RESTRICT** all other modules.
3.  **Decision Support Layer:** Translates the engine's output into a simple, non-prescriptive summary for the user.

For the complete blueprint, see **[docs/architecture.md](docs/architecture.md)**.

## Getting Started

### Prerequisites

-   Python 3.10+
-   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
    cd Misi-Screener
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` will be added in a future update. For now, install `pytest` and `pandas` as needed.)*

### Running Tests

To verify the installation and the integrity of the core modules, run the test suite:

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## Limitations

This is not a predictive tool and does not guarantee any trading outcomes. It is a decision-support system that requires user discretion. The system is designed to say "NO" or "I don't know" frequently.

For a full overview of the system's boundaries, please read **[docs/limitations.md](docs/limitations.md)**.

## Contributing

We welcome contributions that adhere to our strict philosophy. Please read our **[CONTRIBUTING.md](CONTRIBUTING.md)** guide before opening an issue or pull request.
