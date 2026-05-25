# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-03-04

### Added
- **Alpaca Broker Integration**: Real broker connector for both paper and live trading via Alpaca API.
- **Alpaca Data Connector**: Alternative market data source via Alpaca's data API.
- **SQLite Persistence**: Portfolio state, positions, and trade history now persist across restarts using Peewee ORM.
- **Centralized Logging**: Structured logging via `utils/logger.py` with console and file output.
- **Strategy Manager**: Decoupled strategy definitions from trading logic using YAML configuration.
- **ATR Stop-Loss**: RiskManager now supports ATR-based stop-loss calculation with configurable multiplier.
- **Market Hours Awareness**: HedgeFundMasterAgent respects US market hours (9:30 AM - 4:00 PM ET).
- **Async Architecture**: Trading loop uses `asyncio` for non-blocking operation.
- **Docker Support**: Added `Dockerfile` and `docker-compose.yml` for containerized deployment.
- **`.env.example`**: Template for all required API keys (Alpaca, Alpha Vantage, NewsAPI).
- **Models Module**: `agents/models.py` with Peewee ORM models for PortfolioState, Position, Trade.

### Fixed
- **Frontend BigInt Crash**: `formatNumber()` no longer uses `BigInt()` which threw on float/None values. Now uses `Number()` with proper NaN handling.
- **ATR Stop-Loss Key Mismatch**: RiskManager now supports both `atr_multiplier` and `stop_loss_atr_multiplier` YAML keys, ensuring the strategy configuration is properly read.
- **Component Engine Mock Data**: All 9 component engines (macro, monetary, positioning, intermarket, market structure, liquidity, order book, DEX, execution plan, quant scoring, final verdict) no longer return hardcoded placeholder values. They now return clear "not_configured" states with guidance on what data sources are needed.
- **Agent Stub Data**: FundamentalAnalyst, SentimentAnalyst, and TraderAgent no longer return hardcoded mock data. FundamentalAnalyst uses real Alpha Vantage data, SentimentAnalyst uses real NewsAPI data with keyword-based sentiment scoring, and TraderAgent builds proposals from actual signal/price data.
- **Requirements.txt**: Cleaned from 76 transitive dependencies to 14 direct dependencies with proper version specifiers.
- **Technical Analyst Column Names**: Now uses uppercase column names (`High`, `Low`, `Close`) matching yfinance output format.

### Removed
- **Stale Remote Branches**: Deleted 7 stale feature/experiment branches from remote.
- **Old Dashboard UI**: The previous tab-based dashboard has been removed in favor of the terminal interface.
- **Old Monolithic API**: The `/api/v1/analysis` endpoint has been replaced by the modular API.

### Changed
- **README.md**: Rewritten for v2.0.0 with trilingual disclaimers (EN/ID/CN), contributor welcome, and contact information.
- **PortfolioManager**: Now uses Peewee ORM for persistent storage instead of in-memory state.
- **PortfolioManager**: Positions are now valued at market price (with fallback to entry price) instead of always using entry price.
- **RiskManager**: Now takes `data_connector` and `technical_analyst` as dependencies for ATR calculation.

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)

## [1.0.0] - 2024-12-01

### Added
- Initial release of MiSi Screener AI Hedge Fund Platform.
- Core agent architecture (9 agents).
- Component engine framework (11 modules).
- Data source connectors (yfinance, Alpha Vantage, NewsAPI).
- Backtesting engine with "no gimmick" approach.
- FastAPI dashboard backend.
- Interactive terminal frontend.
- Strategy definition via YAML.
- Documentation: ARCHITECTURE.md, philosophy, limitations, validation, references.
