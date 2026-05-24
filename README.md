<p align="center">
  <img src="https://img.shields.io/badge/MiSi-Screener-0A0F1C?style=for-the-badge&logo=data:image/svg+xml;base64,&logoColor=00D4AA" alt="MiSi Screener">
  <img src="https://img.shields.io/badge/Version-1.0.0-00D4AA?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-Unlicense-blue?style=for-the-badge" alt="License">
</p>

<p align="center">
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README.md">English</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_id.md">Bahasa Indonesia</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_zh.md">中文</a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=22&duration=3000&pause=1000&color=00D4AA&center=true&vCenter=true&width=600&lines=AI-Driven+Hedge+Fund+Platform;Autonomous+Trading+Engine;Bloomberg-Grade+Intelligence+Terminal;Modular+Agent-Based+Architecture" alt="Typing SVG" />
</p>

---

## Overview

MiSi Screener is a powerful, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It is architected as a complete ecosystem, functioning as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal**.

The system is designed from the ground up to move beyond analysis into execution, providing all the core components of an automated hedge fund: strategy definition, signal generation, portfolio management, simulated execution, and performance validation through backtesting. This project is part of the [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) ecosystem, a broader initiative to build sovereign-grade, AI-native financial intelligence systems.

## Key Features

- **Autonomous Trading Engine**: A master agent runs a continuous trading loop, executing strategies automatically based on real-time market data. The `HedgeFundMasterAgent` orchestrates signal generation, risk management, and trade execution in a fully autonomous cycle.
- **Strategy Definition via YAML**: Define complex trading strategies with clear, human-readable YAML files, specifying entry/exit conditions, risk management parameters, and position sizing rules. No code changes required to iterate on strategies.
- **"No Gimmick" Backtesting Engine**: A powerful, CLI-based backtester (`run_backtest.py`) that uses the *exact same* components as the live trading engine, ensuring realistic validation of strategy performance without lookahead bias.
- **Operational Dashboard**: The interactive terminal has evolved into a command center. Start and stop the autonomous agent, monitor real-time portfolio performance (`/portfolio`), and conduct market research from a single interface.
- **Modular, Agent-Based Architecture**: The system is composed of specialized agents (`SignalAgent`, `PortfolioManager`, `HedgeFundMasterAgent`) that work together, making the logic clean, decoupled, and extensible.
- **Real-Time Data Integration**: Connects to free, public APIs for all market data, including Yahoo Finance, Alpha Vantage, and NewsAPI, ensuring analysis and trading are grounded in reality.
- **AI Query Orchestrator**: A natural language interface that understands complex queries, identifies multiple tickers, and routes requests to the appropriate data connectors and analytical modules.
- **Quant Scoring Engine**: Proprietary scoring system that aggregates technical, fundamental, and sentiment indicators into a unified quantitative assessment for each asset.

## System Architecture

The project is organized as a complete trading system with clearly separated concerns:

```
Misi-Screener/
├── strategies/           # YAML-based trading strategy definitions
├── agents/               # The "brains": signals, portfolio, orchestration
│   ├── signal_agent.py          # Strategy interpretation & signal generation
│   ├── portfolio_manager.py     # Position sizing & risk management
│   ├── master_agent.py          # Autonomous trading loop orchestrator
│   ├── advanced_orchestrator.py # Natural language query parsing
│   ├── technical_analyst.py     # Technical analysis agent
│   ├── fundamental_analyst.py   # Fundamental analysis agent
│   ├── sentiment_analyst.py     # Market sentiment analysis agent
│   ├── trader_agent.py          # Trade execution agent
│   └── risk_manager.py          # Risk assessment & management
├── components/           # Analytical modules and scoring engines
│   ├── technical_indicators.py  # Core technical indicator calculations
│   ├── quant_scoring/           # Quantitative scoring engine
│   ├── final_verdict/           # Final verdict aggregation engine
│   ├── market_structure/        # Market structure analysis
│   ├── liquidity_orderflow/     # Liquidity & order flow analysis
│   ├── order_book_venue/        # Order book & venue analysis
│   ├── intermarket/             # Intermarket correlation analysis
│   ├── positioning_crowd/       # Crowd positioning analysis
│   ├── dex_intelligence/        # DEX intelligence module
│   ├── macro_analysis/          # Macroeconomic analysis
│   ├── monetary_fundamental/    # Monetary policy fundamental analysis
│   └── execution_plan/          # Execution plan builder
├── execution/            # Simulated paper trading broker
├── data_sources/         # Connectors for external data APIs
│   ├── yfinance_connector.py
│   ├── alpha_vantage_connector.py
│   └── news_connector.py
├── dashboard/            # Interactive web terminal
│   ├── backend/                 # FastAPI backend
│   └── frontend/                # Web UI
├── tests/                # Unit and integration tests
└── run_backtest.py       # Standalone backtesting engine
```

For a more detailed breakdown, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager
- API keys for enhanced features (optional but recommended)

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
```

### 2. Set Up API Keys

Set the following environment variables. While not required for the RSI strategy, they are needed for `/news` and `/FA` commands:

```bash
export NEWS_API_KEY='your_key_from_newsapi.org'
export ALPHA_VANTAGE_API_KEY='your_key_from_alphavantage.co'
```

### 3. Backtesting a Strategy

Before running the agent live, always validate a strategy with the backtester:

```bash
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

This runs the `MeanReversionRSI` strategy over the specified historical period and prints a detailed performance report including total return, drawdown, and trade statistics.

### 4. Running the Autonomous Agent

Start the backend server from the project root:

```bash
python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
```

Then open your web browser to `http://127.0.0.1:8000`.

- Click **"Start Agent"** to initialize the `HedgeFundMasterAgent`. The agent will begin executing its trading loop every 60 seconds by default.
- Use the `/portfolio` command to monitor positions and performance in real-time.
- Click **"Stop Agent"** to gracefully shut down the trading loop.

## Core Agents

| Agent | Module | Role |
|-------|--------|------|
| `HedgeFundMasterAgent` | `agents/master_agent.py` | Master orchestrator running the autonomous trading loop |
| `SignalAgent` | `agents/signal_agent.py` | Strategy interpretation and signal generation (BUY/SELL/HOLD) |
| `PortfolioManager` | `agents/portfolio_manager.py` | Position sizing, risk management, and portfolio state tracking |
| `AdvancedQueryOrchestrator` | `agents/advanced_orchestrator.py` | Natural language query parsing and multi-ticker routing |
| `TechnicalAnalyst` | `agents/technical_analyst.py` | Technical analysis and pattern recognition |
| `FundamentalAnalyst` | `agents/fundamental_analyst.py` | Fundamental analysis and valuation |
| `SentimentAnalyst` | `agents/sentiment_analyst.py` | Market sentiment and news analysis |
| `RiskManager` | `agents/risk_manager.py` | Portfolio risk assessment and management |
| `TraderAgent` | `agents/trader_agent.py` | Trade execution and order management |

## Documentation

- [Architecture Guide](./ARCHITECTURE.md) - Detailed system architecture and component interaction
- [Contributing Guide](./CONTRIBUTING.md) - How to contribute to MiSi Screener
- [Changelog](./CHANGELOG.md) - Release history and notable changes
- [Philosophy](./docs/philosophy.md) - AI-first, sovereign-grade intelligence design philosophy
- [Limitations](./docs/limitations.md) - Current system limitations and known issues
- [Validation](./docs/validation.md) - Strategy validation methodology
- [References](./docs/references.md) - Academic and technical references

## Related Projects

- [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) - The broader AI-native financial intelligence ecosystem
- [SolSniperX](https://github.com/mulkymalikuldhrs/SolSniperX) - AI-powered Solana memecoin sniper bot

## License

This project is released into the public domain under the [Unlicense](./LICENSE). You are free to copy, modify, publish, use, compile, sell, or distribute this software for any purpose, commercial or non-commercial.

## Author

**Mulky Malikul Dhaher**

- Email: mulkymalikuldhaher@email.com
- GitHub: [@mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)

<p align="center">
  <img src="https://img.shields.io/github/stars/mulkymalikuldhrs/Misi-Screener?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/mulkymalikuldhrs/Misi-Screener?style=social" alt="Forks">
  <img src="https://img.shields.io/github/watchers/mulkymalikuldhrs/Misi-Screener?style=social" alt="Watchers">
</p>
