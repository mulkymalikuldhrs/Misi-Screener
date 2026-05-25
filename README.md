<a href="https://github.com/mulkymalikuldhrs/Misi-Screener">
  <img align="center" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=38&duration=3000&pause=1000&color=00D4AA&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=120&lines=MISI+SCREENER+v2.0.0;AI-Driven+Hedge+Fund+Platform;Autonomous+Trading+Engine" alt="Typing SVG" />
</a>

<div align="center">

[![Version](https://img.shields.io/badge/Version-2.0.0-00D4AA?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/mulkymalikuldhrs/Misi-Screener)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/mulkymalikuldhrs/Misi-Screener?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mulkymalikuldhrs/Misi-Screener/stargazers)

</div>

<div align="center">

**Language / Bahasa / 语言**

[![EN](https://img.shields.io/badge/EN-English-blue?style=flat-square)](README.md)
[![ID](https://img.shields.io/badge/ID-Bahasa_Indonesia-red?style=flat-square)](README_id.md)
[![CN](https://img.shields.io/badge/CN-中文-yellow?style=flat-square)](README_zh.md)

</div>

---

## 🇬🇧 English

### Overview

**Misi Screener v2.0.0** is a production-ready, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It functions as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal** — providing all core components of an automated hedge fund: strategy definition, signal generation, portfolio management, execution, and performance validation through backtesting.

> 🔗 Part of the [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) ecosystem — a broader initiative to build sovereign-grade, AI-native financial intelligence systems.

### Key Features

- 🤖 **Autonomous Trading Engine** — Master agent runs continuous trading loop with real-time data
- 📝 **YAML Strategy Definition** — Define complex strategies without code changes
- 📊 **"No Gimmick" Backtesting** — Uses exact same components as live engine
- 🏛️ **Modular Agent Architecture** — 9 specialized agents working in concert
- 💼 **Real Broker Integration** — Support for Alpaca API (Paper & Live trading)
- 💾 **Persistent State** — SQLite + Peewee ORM for portfolio, positions, and trade history
- 🛡️ **ATR-Based Stop Loss** — Volatility-aware risk management with ATR multiplier support
- 📡 **Real-Time Data** — Yahoo Finance, Alpha Vantage, NewsAPI integration
- 🐳 **Docker Ready** — Containerized deployment with docker-compose
- 📋 **Centralized Logging** — Structured logging with file output

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   MISI SCREENER v2.0.0                    │
├─────────────┬──────────────┬──────────────┬──────────────┤
│  STRATEGIES │    AGENTS    │  COMPONENTS  │  DATA LAYER  │
│  (YAML)     │  (9 Agents)  │  (11 Eng.)   │  (4 Sources) │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Entry/Exit  │ Master Agent │ Macro Anal.  │ Yahoo Finance│
│ Risk Mgmt   │ Signal Agent │ Monetary     │ Alpha Vantage│
│ Position    │ Portfolio Mgr│ Positioning  │ NewsAPI      │
│ Sizing      │ Risk Manager │ Intermarket  │ Alpaca       │
│             │ Tech Analyst │ Market Str.  │              │
│             │ Fund. Analyst│ Liquidity    │              │
│             │ Sentiment    │ Order Book   │              │
│             │ Trader Agent │ Exec. Plan   │              │
│             │ Orchestrator │ Quant Score  │              │
│             │              │ Final Verdict│              │
├─────────────┴──────────────┴──────────────┴──────────────┤
│     BACKTESTING ENGINE  │  DASHBOARD (FastAPI)           │
│     Paper Trading       │  Interactive Terminal          │
│     Alpaca Broker       │  SQLite Persistence            │
└──────────────────────────────────────────────────────────┘
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener

# Install dependencies
pip install -r requirements.txt

# Configure API keys (copy and edit .env.example)
cp .env.example .env
# Edit .env with your API keys

# Run backtesting
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"

# Start the dashboard
python main.py
# Access the terminal at http://127.0.0.1:8000
```

### Core Agents

| Agent | Role |
|-------|------|
| `HedgeFundMasterAgent` | Master orchestrator running autonomous trading loop |
| `SignalAgent` | Strategy interpretation and signal generation |
| `PortfolioManager` | Position sizing, risk management, portfolio tracking (SQLite persisted) |
| `RiskManager` | Portfolio risk assessment with ATR stop-loss support |
| `TechnicalAnalyst` | Technical analysis and pattern recognition |
| `FundamentalAnalyst` | Fundamental analysis via Alpha Vantage |
| `SentimentAnalyst` | Market sentiment and news analysis via NewsAPI |
| `TraderAgent` | Trade execution decision synthesis |
| `AdvancedQueryOrchestrator` | Natural language query parsing |

### ⚠️ Disclaimer

**For Education Purpose Only**

This project is provided strictly for educational and research purposes. The authors and contributors assume **no responsibility or liability** for any damages, losses, or risks arising from the use of this software. **We do not bear any responsibility or risk** for how this software is used.

**Contact:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## 🇮🇩 Bahasa Indonesia

### Ringkasan

**Misi Screener v2.0.0** adalah platform sumber terbuka yang siap produksi untuk membangun, menguji, dan menerapkan strategi perdagangan otomatis berbasis AI. Berfungsi sebagai **mesin perdagangan otonom** dan **terminal intelijen tingkat Bloomberg** — menyediakan semua komponen inti hedge fund otomatis: definisi strategi, pembuatan sinyal, manajemen portofolio, eksekusi, dan validasi performa melalui backtesting.

> 🔗 Bagian dari ekosistem [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) — inisiatif lebih luas untuk membangun sistem intelijen keuangan berbasis AI kelas berdaulat.

### Fitur Utama

- 🤖 **Mesin Perdagangan Otonom** — Agen master menjalankan loop perdagangan berkelanjutan
- 📝 **Definisi Strategi YAML** — Tentukan strategi kompleks tanpa perubahan kode
- 📊 **Backtesting Tanpa Tipu** — Menggunakan komponen yang sama persis dengan mesin langsung
- 🏛️ **Arsitektur Agen Modular** — 9 agen khusus bekerja bersama
- 💼 **Integrasi Broker Nyata** — Dukungan Alpaca API (Paper & Live)
- 💾 **Status Persisten** — SQLite + Peewee ORM untuk portofolio dan riwayat perdagangan
- 🛡️ **Stop Loss Berbasis ATR** — Manajemen risiko sadar volatilitas
- 📡 **Data Real-Time** — Yahoo Finance, Alpha Vantage, NewsAPI

### Mulai Cepat

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
cp .env.example .env  # Konfigurasi API key Anda
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

### ⚠️ Disclaimer

**Hanya untuk Tujuan Pendidikan**

Proyek ini disediakan secara ketat untuk tujuan pendidikan dan penelitian. Penulis dan kontributor tidak menanggung **tanggung jawab atau risiko** atas kerusakan, kerugian, atau risiko yang timbul dari penggunaan perangkat lunak ini. **Kami tidak menanggung tanggung jawab atau risiko** atas bagaimana perangkat lunak ini digunakan.

**Kontak:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## 🇨🇳 中文

### 概述

**Misi Screener v2.0.0** 是一个生产就绪的开源平台，用于构建、测试和部署自动化AI驱动的交易策略。它既是**自主交易引擎**，也是**交互式Bloomberg级智能终端**——提供自动化对冲基金的所有核心组件：策略定义、信号生成、投资组合管理、执行和回测验证。

> 🔗 [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) 生态系统的一部分——构建主权级AI原生金融智能系统的更广泛倡议。

### 主要特性

- 🤖 **自主交易引擎** — 主代理运行持续交易循环
- 📝 **YAML策略定义** — 无需代码更改即可定义复杂策略
- 📊 **真实回测引擎** — 使用与实盘引擎完全相同的组件
- 🏛️ **模块化代理架构** — 9个专业代理协同工作
- 💼 **真实券商集成** — 支持Alpaca API（模拟和实盘）
- 💾 **持久化状态** — SQLite + Peewee ORM用于投资组合和交易历史
- 🛡️ **基于ATR的止损** — 感知波动率的风险管理
- 📡 **实时数据** — Yahoo Finance, Alpha Vantage, NewsAPI

### 快速开始

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
cp .env.example .env  # 配置您的API密钥
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

### ⚠️ 免责声明

**仅供教育目的**

本项目严格仅供教育和研究目的。作者和贡献者对因使用本软件而产生的任何损害、损失或风险**不承担任何责任**。**我们不承担任何责任或风险**对于本软件的使用方式。

**联系方式:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## 🤝 Contributing

Contributions are welcome! We encourage the community to help improve this project.

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

Please make sure to update tests as appropriate and follow the PEP 8 code style.

---

## 📚 Documentation

- [Architecture Guide](./ARCHITECTURE.md) — Detailed system architecture
- [Contributing Guide](./CONTRIBUTING.md) — How to contribute
- [Changelog](./CHANGELOG.md) — Release history
- [Code of Conduct](./CODE_OF_CONDUCT.md) — Community standards
- [Security Policy](./SECURITY.md) — Security reporting

## 🔗 Related Projects

| Project | Description |
|---------|-------------|
| [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) | Autonomous multi-agent trading infrastructure |
| [Quant-Nanggroe-AI](https://github.com/mulkymalikuldhrs/Quant-Nanggroe-AI) | Multi-Agent Decision Intelligence OS |
| [AI-MultiColony-Ecosystem](https://github.com/mulkymalikuldhrs/AI-MultiColony-Ecosystem) | Multi-agent colony coordination platform |
| [cyber-shell-x-nexus](https://github.com/mulkymalikuldhrs/cyber-shell-x-nexus) | Advanced cybersecurity platform with AI assistant |

## 📬 Contact

<div align="center">

[![Email](https://img.shields.io/badge/Email-mulkymalikuldhaher@email.com-00D4AA?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mulkymalikuldhaher@email.com)
[![GitHub](https://img.shields.io/badge/GitHub-mulkymalikuldhrs-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mulkymalikuldhrs)

</div>

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D9488,50:065F46,100:020205&height=100&section=footer" width="100%" />

Built with 💎 by **Mulky Malikul Dhaher** 🇮🇩

</div>
