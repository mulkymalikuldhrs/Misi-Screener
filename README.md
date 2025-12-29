# MiSi Screener - Sovereign Grade Intelligence Dashboard

This repository contains the source code for the MiSi Screener, a sophisticated, AI-powered quantitative analysis dashboard designed for traders and analysts who require deep, multi-faceted market insights.

The system is built on a non-predictive, risk-first philosophy, providing decision-support tools rather than simple buy/sell signals. It integrates a comprehensive backend API with a reactive, user-friendly frontend to deliver a seamless analysis experience.

## Core Features

-   **Unified Analysis API**: A single, powerful API endpoint delivers a complete, structured analysis for any given asset, covering everything from market structure to macro context.
-   **Interactive Charting**: High-performance candlestick charts powered by TradingView Lightweight Charts™.
-   **AI-Powered Reporting**: Dynamically generated reports from 11 core analytical modules, providing a 360-degree view of the asset.
-   **Integrated Risk Management**: A built-in position size calculator to enforce disciplined risk-taking.
-   **Modular & Scalable**: A clean architecture that separates the frontend, backend, and core analytical components, making it easy to extend and maintain.

## Tech Stack

-   **Backend**: Python 3, FastAPI
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
-   **Charting**: TradingView Lightweight Charts™

## System Architecture

The project is organized into two main parts: the `dashboard` and the core `components`.

### 1. Dashboard (`dashboard/`)

This directory contains the user-facing application.

-   `frontend/index.html`: The main single-page application (SPA). It handles the UI, user interactions, and data visualization.
-   `backend/main.py`: A FastAPI server that exposes the data API and serves the frontend.

#### API Endpoint

The backend provides one primary endpoint:

-   `GET /api/v1/analysis?asset={asset_name}`

This endpoint returns a `FullAnalysisResponse` JSON object containing:
-   `asset`: The name of the asset.
-   `chart_data`: An array of OHLCV candles for the charting tab.
-   `ai_analysis`: A detailed report object with insights from all 11 analytical modules.
-   `technical_details`: A summary of key technical indicator values.

### 2. Analytical Core (`components/`)

This directory holds the Python stubs for the 11 core analytical modules that form the "brain" of the system. In a production environment, these modules would contain the complex logic for generating real analysis.

## Getting Started

### Prerequisites

-   Python 3.8+
-   `pip` for package management

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

3.  **Navigate to the backend directory and run the server:**
    ```bash
    cd dashboard/backend
    uvicorn main:app --reload
    ```
    The server will start, typically on `http://127.0.0.1:8000`.

4.  **Access the dashboard:**
    Open your web browser and navigate to `http://127.0.0.1:8000`. The frontend application will be served automatically.

## Philosophy

MiSi Screener is designed to be a market intelligence system that helps traders understand market context, not to predict prices. It operates on the principles of being non-predictive, risk-first, regime-aware, and deterministic.

(For more details, see `docs/philosophy.md` and `docs/architecture.md`)
