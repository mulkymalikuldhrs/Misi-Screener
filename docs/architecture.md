# MiSi AI Hedge Fund - Architecture

The MiSi AI Hedge Fund is an autonomous trading platform designed for real-time market analysis and automated trade execution. The system follows a decoupled, agent-based architecture where specialized agents handle specific parts of the trading lifecycle.

## Core Components

### 1. HedgeFundMasterAgent (`agents/hedge_fund_master_agent.py`)
The orchestrator of the system. It runs an asynchronous trading loop, coordinating signals from the `SignalAgent`, risk assessment from the `RiskManager`, and execution through the `Broker`.

### 2. StrategyManager (`agents/strategy_manager.py`)
Responsible for loading and parsing trading strategies defined in YAML files. It provides a standardized interface for other agents to access strategy parameters and risk rules.

### 3. SignalAgent (`agents/signal_agent.py`)
Generates trading signals (BUY, SELL, HOLD) based on the current strategy. It uses the `TechnicalAnalystAgent` to calculate indicators and the `DataConnector` to fetch historical data.

### 4. TechnicalAnalystAgent (`agents/technical_analyst.py`)
A specialized agent for technical analysis. It encapsulates the logic for calculating indicators like RSI, MACD, and ATR, providing a clean API for other agents.

### 5. PortfolioManager (`agents/portfolio_manager.py`)
Manages the global state of the fund, including cash balances, open positions, and trade history. It performs real-time portfolio valuation and calculates position sizes based on risk parameters.

### 6. RiskManager (`agents/risk_manager.py`)
Centralizes all risk-related calculations. Its primary role is to determine appropriate stop-loss levels (e.g., ATR-based) and ensure that every trade adheres to the fund's risk management policy.

### 7. PaperTradingBroker (`execution/paper_trading_broker.py`)
Simulates a real-world broker. It executes trades with realistic frictions, including slippage and commission fees, and updates the `PortfolioManager`.

## Data Layer
The system uses specialized connectors (`data_sources/`) to fetch data from external APIs like Yahoo Finance, Alpha Vantage, and NewsAPI.

## Dashboard & API
The system features a Bloomberg-grade operational terminal.
- **Backend**: A FastAPI application (`dashboard/backend/main.py`) that orchestrates the agents and provides REST endpoints for control and monitoring.
- **Frontend**: An interactive web interface (`dashboard/frontend/index.html`) for real-time visualization and manual command override.

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
