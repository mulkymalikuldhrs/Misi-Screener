# MiSi Screener - Sovereign Grade AI Intelligence System

## Overview

MiSi Screener is a next-generation, AI-native financial analysis platform designed to function as both a **fully autonomous trading agent** and an **interactive, Bloomberg-grade intelligence terminal** for human analysts.

The system's core philosophy is to leverage cutting-edge AI to orchestrate complex data gathering, analysis, and strategy execution, moving beyond static dashboards into a dynamic, AI-driven analytical environment.

## Key Features

-   **Dual-Mode Operation**: Can be run headless as an autonomous agent or interactively via a sophisticated terminal UI.
-   **AI-Powered Orchestration**: A central AI agent parses natural language queries, invokes the appropriate analytical modules, and synthesizes results.
-   **Modular & Extensible Architecture**: Built with distinct, swappable components for data sources, analysis, and strategy execution, inspired by professional-grade systems like OpenBB.
-   **Bloomberg-Style Terminal**: A multi-panel, command-driven user interface for rapid, keyboard-first analysis.
-   **Real-Time Data Integration**: Connects to a wide array of free, public APIs for market data, news, and fundamental analysis.

## Tech Stack

-   **Backend**: Python 3, FastAPI
-   **AI Agent Framework**: (Placeholder for future implementation)
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
-   **Data Connectors**: `yfinance`, `newsapi-python`, `requests`

## System Architecture

The project is architected to support its dual-mode vision:

-   `agents/`: Contains the core logic for the AI orchestrator and future autonomous trading agents.
-   `data_sources/`: Holds modular connectors for fetching data from various external APIs.
-   `dashboard/`: The interactive terminal application, comprised of a FastAPI backend and a vanilla JS frontend.
-   `components/`: (Future Use) Will contain standalone, reusable analytical modules (e.g., for complex TA or risk modeling).
-   `tests/`: Unit and integration tests for the system.

(For a more detailed breakdown, please see `docs/architecture.md` and `docs/philosophy.md`.)

## Getting Started

### Prerequisites

-   Python 3.9+
-   An environment variable set for `NEWS_API_KEY` (from newsapi.org).
-   An environment variable set for `ALPHA_VANTAGE_API_KEY` (from alphavantage.co).

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
    cd Misi-Screener
    ```

2.  **Install dependencies from the root directory:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the terminal's backend server:**
    ```bash
    python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    *Note: The server is run from the project root to ensure correct module resolution.*

4.  **Access the Terminal:**
    Open your web browser and navigate to `http://127.0.0.1:8000`. Click on any panel to open the command palette (`Ctrl+K`).
