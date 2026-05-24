<a href="https://github.com/mulkymalikuldhrs/Misi-Screener">
  <img align="center" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=38&duration=3000&pause=1000&color=00D4AA&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=120&lines=MISI+SCREENER;AI-Driven+Hedge+Fund+Platform;Autonomous+Trading+Engine" alt="Typing SVG" />
</a>

<div align="center">

[![Version](https://img.shields.io/badge/Version-1.0.0-00D4AA?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/mulkymalikuldhrs/Misi-Screener)
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

**Misi Screener** is a powerful, open-source platform for building, testing, and deploying automated, AI-driven trading strategies. It functions as both an **autonomous trading engine** and an **interactive, Bloomberg-grade intelligence terminal** — providing all core components of an automated hedge fund: strategy definition, signal generation, portfolio management, simulated execution, and performance validation through backtesting.

> 🔗 Part of the [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) ecosystem — a broader initiative to build sovereign-grade, AI-native financial intelligence systems.

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   MISI SCREENER PLATFORM                  │
├─────────────┬──────────────┬──────────────┬──────────────┤
│  STRATEGIES │    AGENTS    │  COMPONENTS  │  DATA LAYER  │
│  (YAML)     │  (9 Agents)  │  (12 Eng.)   │  (3 Sources) │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Entry/Exit  │ Master Agent │ Quant Score  │ Yahoo Finance│
│ Risk Mgmt   │ Signal Agent │ Market Str.  │ Alpha Vantage│
│ Position    │ Portfolio Mgr│ Liquidity    │ News API     │
│ Sizing      │ Risk Manager │ DEX Intel    │              │
│             │ Tech Analyst │ Macro Anal.  │              │
│             │ Fund. Analyst│ Order Book   │              │
│             │ Sentiment    │ Execution    │              │
│             │ Trader Agent │ Final Verdict│              │
│             │ Orchestrator │ Intermarket  │              │
├─────────────┴──────────────┴──────────────┴──────────────┤
│           BACKTESTING ENGINE  │  DASHBOARD (FastAPI)      │
│           Paper Trading       │  Interactive Terminal     │
└──────────────────────────────────────────────────────────┘
```

### Key Features

- 🤖 **Autonomous Trading Engine** — Master agent runs continuous trading loop with real-time data
- 📝 **YAML Strategy Definition** — Define complex strategies without code changes
- 📊 **"No Gimmick" Backtesting** — Uses exact same components as live engine
- 🏛️ **Modular Agent Architecture** — 9 specialized agents working in concert
- 📈 **Quant Scoring Engine** — Aggregates technical, fundamental & sentiment indicators
- 🔍 **AI Query Orchestrator** — Natural language interface for multi-ticker analysis
- 📡 **Real-Time Data** — Yahoo Finance, Alpha Vantage, NewsAPI integration

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener

# Install dependencies
pip install -r requirements.txt

# Run backtesting
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"

# Start the dashboard
python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
```

### Core Agents

| Agent | Role |
|-------|------|
| `HedgeFundMasterAgent` | Master orchestrator running autonomous trading loop |
| `SignalAgent` | Strategy interpretation and signal generation |
| `PortfolioManager` | Position sizing, risk management, portfolio tracking |
| `AdvancedQueryOrchestrator` | Natural language query parsing |
| `TechnicalAnalyst` | Technical analysis and pattern recognition |
| `FundamentalAnalyst` | Fundamental analysis and valuation |
| `SentimentAnalyst` | Market sentiment and news analysis |
| `RiskManager` | Portfolio risk assessment |
| `TraderAgent` | Trade execution and order management |

---

## 🇮🇩 Bahasa Indonesia

### Ringkasan

**Misi Screener** adalah platform sumber terbuka yang kuat untuk membangun, menguji, dan menerapkan strategi perdagangan otomatis berbasis AI. Berfungsi sebagai **mesin perdagangan otonom** dan **terminal intelijen tingkat Bloomberg** — menyediakan semua komponen inti hedge fund otomatis: definisi strategi, pembuatan sinyal, manajemen portofolio, eksekusi simulasi, dan validasi performa melalui backtesting.

> 🔗 Bagian dari ekosistem [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) — inisiatif lebih luas untuk membangun sistem intelijen keuangan berbasis AI kelas berdaulat.

### Fitur Utama

- 🤖 **Mesin Perdagangan Otonom** — Agen master menjalankan loop perdagangan berkelanjutan
- 📝 **Definisi Strategi YAML** — Tentukan strategi kompleks tanpa perubahan kode
- 📊 **Backtesting Tanpa Tipu** — Menggunakan komponen yang sama persis dengan mesin langsung
- 🏛️ **Arsitektur Agen Modular** — 9 agen khusus bekerja bersama
- 📈 **Mesin Skor Kuant** — Menggabungkan indikator teknikal, fundamental & sentimen
- 🔍 **Orkestrator Kueri AI** — Antarmuka bahasa alami untuk analisis multi-ticker

### Mulai Cepat

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

---

## 🇨🇳 中文

### 概述

**Misi Screener** 是一个强大的开源平台，用于构建、测试和部署自动化AI驱动的交易策略。它既是**自主交易引擎**，也是**交互式Bloomberg级智能终端**——提供自动化对冲基金的所有核心组件：策略定义、信号生成、投资组合管理、模拟执行和回测验证。

> 🔗 [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) 生态系统的一部分——构建主权级AI原生金融智能系统的更广泛倡议。

### 主要特性

- 🤖 **自主交易引擎** — 主代理运行持续交易循环
- 📝 **YAML策略定义** — 无需代码更改即可定义复杂策略
- 📊 **真实回测引擎** — 使用与实盘引擎完全相同的组件
- 🏛️ **模块化代理架构** — 9个专业代理协同工作
- 📈 **量化评分引擎** — 聚合技术、基本面和情绪指标
- 🔍 **AI查询协调器** — 多股票分析自然语言接口

### 快速开始

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

---

## ⚠️ Disclaimer

**For Education Purpose Only**

This project is provided strictly for educational and research purposes. The authors and contributors assume **no responsibility or liability** for any damages, losses, or risks arising from the use of this software. **We do not bear any responsibility or risk** for how this software is used.

**Contact:** Mulky Malikul Dhaher | mulkymalikuldhaher@email.com

---

## 📚 Documentation

- [Architecture Guide](./ARCHITECTURE.md) — Detailed system architecture
- [Contributing Guide](./CONTRIBUTING.md) — How to contribute
- [Changelog](./CHANGELOG.md) — Release history
- [Philosophy](./docs/philosophy.md) — AI-first design philosophy
- [Limitations](./docs/limitations.md) — Known issues
- [Validation](./docs/validation.md) — Strategy validation methodology

## 🔗 Related Projects

| Project | Description |
|---------|-------------|
| [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) | Autonomous multi-agent trading infrastructure |
| [Quant-Nanggroe-AI](https://github.com/mulkymalikuldhrs/Quant-Nanggroe-AI) | Multi-Agent Decision Intelligence OS |
| [AI-MultiColony-Ecosystem](https://github.com/mulkymalikuldhrs/AI-MultiColony-Ecosystem) | Multi-agent colony coordination platform |

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
