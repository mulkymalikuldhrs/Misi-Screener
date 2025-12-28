# MiSi Screener Architecture

## System Overview

MiSi Screener is a market intelligence system designed to provide non-predictive, regime-aware decision support for traders. It is built on a modular, production-grade architecture that prioritizes clarity, auditability, and risk management.

## Core Components

The system is organized into several key domains, each with a specific responsibility:

### 1. Data Pipeline (`data/`)

The data pipeline is responsible for ingesting, validating, and preparing market data for analysis.

- **Loaders (`data/loaders/`):** Ingest raw data (e.g., OHLCV) from various sources.
- **Validators (`data/validators/`):** Ensure data integrity by checking for gaps, duplicates, and anomalies.
- **Features (`data/features/`):** Extract quantitative features from the validated data.

### 2. Core Quant Engine (`core/`)

This is the analytical heart of the system.

- **Market Structure (`core/structure/`):** Analyzes price action to identify trends, swing points (HH/HL/LH/LL), and structural breaks (BOS/CHoCH).
- **Liquidity & Participation (`core/liquidity/`):** Measures market activity, volume, and range dynamics to assess participation and detect potential exhaustion or continuation.
- **Regime Classification (`core/regime/`):** The central engine that synthesizes inputs from other modules to classify the current market regime (e.g., Expansion, Compression, Transition).
- **Risk Governor (`core/risk/`):** A master control module that assesses systemic risk based on volatility, drawdown, and correlation stress. It has the authority to issue `ALLOW`, `RESTRICT`, or `BLOCK` directives that gate all other system outputs.
- **Decision Support (`core/decision_support/`):** Aggregates the outputs from the quant engine into a clear, concise summary for the end-user, including market state, regime, and risk level.

### 3. API (`api/`)

Exposes the system's output via a FastAPI interface.

### 4. Frontend (`frontend/`)

Provides a user interface for visualizing the system's output.

- **Charts (`frontend/charts/`):** Displays market data and the system's analysis.

### 5. Documentation (`docs/`)

Contains all project documentation, including this file.

### 6. Tests (`tests/`)

Contains unit and integration tests for the system.
