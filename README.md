# MiSi Screener - AI-Driven Hedge Fund Platform

## Overview

MiSi Screener is a production-ready, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It functions as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal**.

The system is designed for real-world execution, providing persistence, real broker integration, and advanced risk management.

## Key Features

-   **Autonomous Trading Engine**: A master agent runs a continuous trading loop, executing strategies automatically.
-   **Real Broker Integration**: Support for **Alpaca API** (Paper and Live), moving beyond simple simulations.
-   **Persistent State**: Uses SQLite and Peewee ORM to ensure your portfolio, positions, and trade history survive restarts.
-   **Strategy Definition via YAML**: Define complex trading strategies with clear YAML files, supporting multi-asset portfolios.
-   **Production-Ready**:
    - Centralized logging.
    - Market hour awareness (respects US market hours).
    - Robust error handling and retries.
    - Containerized deployment with Docker.
-   **Operational Dashboard**: Interactive terminal for monitoring real-time portfolio performance, news, and research.

## System Architecture

```
Misi-Screener/
│
├── agents/               # Core AI agents (Signals, Portfolio, Risk, Master)
├── data_sources/         # Connectors (Alpaca, YFinance, NewsAPI, etc.)
├── execution/            # Broker connectors (Alpaca, Paper)
├── dashboard/            # FastAPI backend and web frontend
├── utils/                # Shared utilities (Logger)
├── strategies/           # Strategy definitions (YAML)
├── tests/                # Comprehensive test suite
├── Dockerfile            # Container definition
└── docker-compose.yml    # Multi-container orchestration
```

## Getting Started

### 1. Installation

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
pip install alpaca-trade-api
```

### 2. Configuration

Set the following environment variables:

```bash
export ALPACA_API_KEY='your_alpaca_key'
export ALPACA_API_SECRET='your_alpaca_secret'
export ALPACA_BASE_URL='https://paper-api.alpaca.markets'
export NEWS_API_KEY='your_news_api_key'
export ALPHA_VANTAGE_API_KEY='your_alpha_vantage_key'
```

### 3. Running with Docker (Recommended)

```bash
docker-compose up -d
```

### 4. Running Locally

1.  **Start the platform:**
    ```bash
    python main.py
    ```

2.  **Access the Terminal:**
    Open `http://127.0.0.1:8000`.

## Strategy Customization

Modify `strategies/mean_reversion_rsi.yml` to change parameters or add multiple assets:

```yaml
name: "MeanReversionRSI"
asset_tickers: ["AAPL", "MSFT", "TSLA"]
timeframe: "1Hour"
parameters:
  rsi_period: 14
  oversold_threshold: 30
  overbought_threshold: 70
risk_management:
  risk_per_trade_percent: 1.0
  stop_loss_method: "atr"
  atr_multiplier: 2.0
```

## License

MIT License.
---

## 🤝 Contributing

Contributions are welcome! We encourage the community to help improve this project.

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

Please make sure to update tests as appropriate and follow the existing code style.

---

## 📬 Contact

**Mulky Malikul Dhaher** — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)

GitHub: [https://github.com/mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)

---

## ⚠️ Disclaimer

**This project is for Education Purpose only.**

All content, code, and documentation provided in this repository are intended solely for educational and research purposes. Nothing in this repository constitutes financial, investment, legal, or professional advice.

**Risiko apapun tidak kita tanggung.** (We are not responsible for any risks or damages.)

Use at your own risk. The authors and contributors assume no liability for any losses, damages, or consequences arising from the use of this software or information provided herein.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Copyright © Mulky Malikul Dhaher. All rights reserved.

