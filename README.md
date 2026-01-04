# MiSi Screener - AI-Driven Hedge Fund Platform

## Overview

MiSi Screener has evolved into a powerful, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It is architected as a complete ecosystem, functioning as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal**.

The system is designed from the ground up to move beyond analysis into execution, providing all the core components of an automated hedge fund: strategy definition, signal generation, portfolio management, simulated execution, and performance validation through backtesting.

## Key Features

-   **Autonomous Trading Engine**: A master agent runs a continuous trading loop, executing strategies automatically based on real-time market data.
-   **Strategy Definition via YAML**: Define complex trading strategies with clear, human-readable YAML files, specifying entry/exit conditions and risk management parameters.
-   **"No Gimmick" Backtesting Engine**: A powerful, CLI-based backtester (`run_backtest.py`) that uses the *exact same* components as the live trading engine, ensuring realistic validation of strategy performance.
-   **Operational Dashboard**: The interactive terminal has evolved into a command center. Start and stop the autonomous agent, monitor real-time portfolio performance (`/portfolio`), and conduct market research from a single interface.
-   **Modular, Agent-Based Architecture**: The system is composed of specialized agents (`SignalAgent`, `PortfolioManager`, `HedgeFundMasterAgent`) that work together, making the logic clean, decoupled, and extensible.
-   **Real-Time Data Integration**: Continues to connect to free, public APIs for all market data, ensuring analysis and trading are grounded in reality.

## System Architecture

The project has been transformed into a complete trading system:

-   `strategies/`: Contains YAML files that define the logic for trading strategies.
-   `agents/`: The "brain" of the system, containing all agents responsible for signals, portfolio management, and master orchestration.
-   `execution/`: A simulated paper trading broker that executes trades with realism.
-   `dashboard/`: The interactive web terminal for monitoring and control.
-   `run_backtest.py`: A powerful command-line tool for validating strategies on historical data.

(For a more detailed breakdown, please see `docs/architecture.md`.)

## Getting Started

### 1. Installation

1.  **Clone the repository and install dependencies:**
    ```bash
    git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
    cd Misi-Screener
    pip install -r requirements.txt
    ```

2.  **Set up API Keys:**
    Set the following environment variables. While not required for the RSI strategy, they are needed for `/news` and `/FA` commands.
    ```bash
    export NEWS_API_KEY='your_key_from_newsapi.org'
    export ALPHA_VANTAGE_API_KEY='your_key_from_alphavantage.co'
    ```

### 2. Backtesting a Strategy

Before running the agent live, always validate a strategy with the backtester.

1.  **Run the backtest from the command line:**
    ```bash
    python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
    ```
    This will run the `MeanReversionRSI` strategy over the specified historical period and print a performance report.

### 3. Running the Autonomous Agent

1.  **Start the backend server from the project root:**
    ```bash
    python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Access the Terminal:**
    Open your web browser to `http://127.0.0.1:8000`.

3.  **Deploy the Agent:**
    -   Click the **"Start Agent"** button. This will initialize and deploy the `HedgeFundMasterAgent` in the background. The agent will begin executing its trading loop every 60 seconds (by default).
    -   Use the `/portfolio` command in any panel to monitor your positions and performance in real-time.
    -   Click **"Stop Agent"** to gracefully shut down the trading loop.
