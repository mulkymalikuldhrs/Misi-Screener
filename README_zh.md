<p align="center">
  <img src="https://img.shields.io/badge/MiSi-Screener-0A0F1C?style=for-the-badge&logo=data:image/svg+xml;base64,&logoColor=00D4AA" alt="MiSi Screener">
  <img src="https://img.shields.io/badge/版本-1.0.0-00D4AA?style=for-the-badge" alt="版本">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/许可证-Unlicense-blue?style=for-the-badge" alt="许可证">
</p>

<p align="center">
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README.md">English</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_id.md">Bahasa Indonesia</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_zh.md">中文</a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=22&duration=3000&pause=1000&color=00D4AA&center=true&vCenter=true&width=600&lines=AI驱动的对冲基金平台;自主交易引擎;彭博级智能终端;模块化代理架构" alt="Typing SVG" />
</p>

---

## 概述

MiSi Screener 是一个功能强大的开源平台，用于构建、测试和部署 AI 驱动的自动化交易策略。它被架构为一个完整的生态系统，兼具**自主交易引擎**和**交互式彭博级智能终端**的双重功能。

该系统从底层设计就超越了分析走向执行，提供了自动化对冲基金的所有核心组件：策略定义、信号生成、投资组合管理、模拟执行以及通过回测进行的绩效验证。本项目是 [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) 生态系统的一部分，该生态系统是构建主权级 AI 原生金融智能系统的更广泛倡议。

## 核心特性

- **自主交易引擎**：主代理运行持续的交易循环，根据实时市场数据自动执行策略。`HedgeFundMasterAgent` 在完全自主的循环中协调信号生成、风险管理和交易执行。
- **基于 YAML 的策略定义**：通过清晰、人类可读的 YAML 文件定义复杂交易策略，指定入场/出场条件、风险管理参数和仓位规模规则。迭代策略无需修改代码。
- **"无噱头"回测引擎**：强大的基于 CLI 的回测器（`run_backtest.py`）使用与实盘交易引擎*完全相同*的组件，确保策略绩效的真实验证，避免前瞻偏差。
- **运营仪表板**：交互式终端已进化为指挥中心。启动和停止自主代理，监控实时投资组合绩效（`/portfolio`），并在单一界面进行市场研究。
- **模块化代理架构**：系统由专门的代理（`SignalAgent`、`PortfolioManager`、`HedgeFundMasterAgent`）组成，它们协同工作，使逻辑清晰、解耦且可扩展。
- **实时数据集成**：连接免费公共 API 获取所有市场数据，包括 Yahoo Finance、Alpha Vantage 和 NewsAPI，确保分析和交易基于真实数据。
- **AI 查询协调器**：自然语言接口，能够理解复杂查询、识别多个股票代码，并将请求路由到适当的数据连接器和分析模块。
- **量化评分引擎**：专有评分系统，将技术面、基本面和情绪指标聚合为每个资产的统一量化评估。

## 系统架构

项目被组织为一个完整的交易系统，职责清晰分离：

```
Misi-Screener/
├── strategies/           # 基于 YAML 的交易策略定义
├── agents/               # "大脑"：信号、投资组合、协调
│   ├── signal_agent.py          # 策略解释与信号生成
│   ├── portfolio_manager.py     # 仓位规模与风险管理
│   ├── master_agent.py          # 自主交易循环协调器
│   ├── advanced_orchestrator.py # 自然语言查询解析
│   ├── technical_analyst.py     # 技术分析代理
│   ├── fundamental_analyst.py   # 基本面分析代理
│   ├── sentiment_analyst.py     # 市场情绪分析代理
│   ├── trader_agent.py          # 交易执行代理
│   └── risk_manager.py          # 风险评估与管理
├── components/           # 分析模块和评分引擎
│   ├── technical_indicators.py  # 核心技术指标计算
│   ├── quant_scoring/           # 量化评分引擎
│   ├── final_verdict/           # 最终裁决聚合引擎
│   ├── market_structure/        # 市场结构分析
│   ├── liquidity_orderflow/     # 流动性与订单流分析
│   ├── order_book_venue/        # 订单簿与场所分析
│   ├── intermarket/             # 跨市场相关性分析
│   ├── positioning_crowd/       # 人群仓位分析
│   ├── dex_intelligence/        # DEX 智能模块
│   ├── macro_analysis/          # 宏观经济分析
│   ├── monetary_fundamental/    # 货币政策基本面分析
│   └── execution_plan/          # 执行计划构建器
├── execution/            # 模拟纸交易经纪商
├── data_sources/         # 外部数据 API 连接器
│   ├── yfinance_connector.py
│   ├── alpha_vantage_connector.py
│   └── news_connector.py
├── dashboard/            # 交互式 Web 终端
│   ├── backend/                 # FastAPI 后端
│   └── frontend/                # Web 用户界面
├── tests/                # 单元和集成测试
└── run_backtest.py       # 独立回测引擎
```

更详细的说明请参阅 [ARCHITECTURE.md](./ARCHITECTURE.md)。

## 快速开始

### 前提条件

- Python 3.11 或更高版本
- pip 包管理器
- API 密钥（可选但推荐用于增强功能）

### 1. 安装

克隆仓库并安装依赖项：

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
```

### 2. 设置 API 密钥

设置以下环境变量。虽然 RSI 策略不需要，但 `/news` 和 `/FA` 命令需要：

```bash
export NEWS_API_KEY='your_key_from_newsapi.org'
export ALPHA_VANTAGE_API_KEY='your_key_from_alphavantage.co'
```

### 3. 回测策略

在实盘运行代理之前，务必使用回测器验证策略：

```bash
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

这将在指定的历史期间运行 `MeanReversionRSI` 策略，并打印详细的绩效报告，包括总回报、回撤和交易统计。

### 4. 运行自主代理

从项目根目录启动后端服务器：

```bash
python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
```

然后在浏览器中打开 `http://127.0.0.1:8000`。

- 点击 **"Start Agent"** 初始化 `HedgeFundMasterAgent`。代理将默认每 60 秒执行一次交易循环。
- 使用 `/portfolio` 命令实时监控持仓和绩效。
- 点击 **"Stop Agent"** 优雅地关闭交易循环。

## 核心代理

| 代理 | 模块 | 角色 |
|------|------|------|
| `HedgeFundMasterAgent` | `agents/master_agent.py` | 运行自主交易循环的主协调器 |
| `SignalAgent` | `agents/signal_agent.py` | 策略解释和信号生成（买入/卖出/持有） |
| `PortfolioManager` | `agents/portfolio_manager.py` | 仓位规模、风险管理和投资组合状态跟踪 |
| `AdvancedQueryOrchestrator` | `agents/advanced_orchestrator.py` | 自然语言查询解析和多股票代码路由 |
| `TechnicalAnalyst` | `agents/technical_analyst.py` | 技术分析和模式识别 |
| `FundamentalAnalyst` | `agents/fundamental_analyst.py` | 基本面分析和估值 |
| `SentimentAnalyst` | `agents/sentiment_analyst.py` | 市场情绪和新闻分析 |
| `RiskManager` | `agents/risk_manager.py` | 投资组合风险评估和管理 |
| `TraderAgent` | `agents/trader_agent.py` | 交易执行和订单管理 |

## 文档

- [架构指南](./ARCHITECTURE.md) - 详细的系统架构和组件交互
- [贡献指南](./CONTRIBUTING.md) - 如何为 MiSi Screener 做贡献
- [更新日志](./CHANGELOG.md) - 发布历史和重要变更
- [设计哲学](./docs/philosophy.md) - AI 优先的主权级智能设计哲学
- [局限性](./docs/limitations.md) - 当前系统限制和已知问题
- [验证](./docs/validation.md) - 策略验证方法论
- [参考文献](./docs/references.md) - 学术和技术参考

## 相关项目

- [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) - 更广泛的 AI 原生金融智能生态系统
- [SolSniperX](https://github.com/mulkymalikuldhrs/SolSniperX) - AI 驱动的 Solana 迷因币狙击机器人

## 许可证

本项目根据 [Unlicense](./LICENSE) 发布到公共领域。您可以出于任何目的（商业或非商业）自由复制、修改、发布、使用、编译、出售或分发本软件。

## 作者

**Mulky Malikul Dhaher**

- 电子邮件：mulkymalikuldhaher@email.com
- GitHub：[@mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)

<p align="center">
  <img src="https://img.shields.io/github/stars/mulkymalikuldhrs/Misi-Screener?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/mulkymalikuldhrs/Misi-Screener?style=social" alt="Forks">
  <img src="https://img.shields.io/github/watchers/mulkymalikuldhrs/Misi-Screener?style=social" alt="Watchers">
</p>
