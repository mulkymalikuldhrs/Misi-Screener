# MiSi Screener - AI-Driven Hedge Fund Platform

## Overview

MiSi Screener is a production-grade, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It is architected as a complete ecosystem, functioning as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal**.

The system provides all the core components of an automated hedge fund: strategy definition, signal generation, portfolio management, risk control, simulated execution, and performance validation through backtesting.

## Key Features

-   **Autonomous Trading Engine**: An asynchronous master agent orchestrates a continuous trading loop, executing strategies automatically based on real-time market data.
-   **Modular Agent Architecture**: Specialized agents (`SignalAgent`, `PortfolioManager`, `RiskManager`, `TechnicalAnalystAgent`) ensure clean separation of concerns and production-ready reliability.
-   **Real-Time Portfolio Valuation**: Positions are valued in real-time using live market data, providing accurate P&L tracking and dynamic position sizing.
-   **Advanced Risk Management**: Integrated ATR-based stop-loss and risk-adjusted sizing protect capital during market volatility.
-   **Realistic Execution Simulation**: The `PaperTradingBroker` accounts for trading frictions like slippage and commission fees for high-fidelity performance estimation.
-   **"No Gimmick" Backtesting**: A standalone CLI tool (`run_backtest.py`) validates strategies on historical data using the *exact same* logic as the live trading engine.
-   **Operational Dashboard**: A terminal-inspired UI for real-time monitoring, manual overrides, and market research.

## System Architecture

The project is organized into specialized modules:

-   `agents/`: Core AI logic including orchestration, signals, risk management, and portfolio state.
-   `strategies/`: YAML-based strategy definitions (e.g., RSI thresholds, risk parameters).
-   `execution/`: Realistic paper trading broker with slippage and fee modeling.
-   `data_sources/`: Connectors for Yahoo Finance, Alpha Vantage, and NewsAPI.
-   `components/`: Low-level technical indicator and analysis engines.
-   `dashboard/`: FastAPI backend and interactive frontend terminal.

(For a detailed breakdown, please see `docs/architecture.md`.)

## Getting Started

### 1. Installation

1.  **Clone the repository and install dependencies:**
    ```bash
    git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
    cd Misi-Screener
    pip install -r requirements.txt
    ```

2.  **Set up API Keys (Optional):**
    ```bash
    export NEWS_API_KEY='your_key'
    export ALPHA_VANTAGE_API_KEY='your_key'
    ```

### 2. Backtesting a Strategy

```bash
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

### 3. Running the Autonomous Agent

1.  **Start the backend server:**
    ```bash
    python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Access the Terminal:** `http://127.0.0.1:8000`

3.  **Deploy**: Click **"Start Agent"** to begin autonomous trading. Use `/portfolio` to monitor live performance.
