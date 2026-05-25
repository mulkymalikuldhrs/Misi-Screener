# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-05-20

### Added
-   **New AI Terminal Architecture**: Complete project overhaul to establish the foundation for a Bloomberg-grade AI terminal.
-   **Modular Data Sources**: Created a new `data_sources` directory with connectors for `yfinance` (market data), `NewsAPI` (news), and `Alpha Vantage` (fundamentals).
-   **AI Agent Orchestrator**: Added an `agents` directory with a foundational `QueryOrchestrator` to parse natural language queries.
-   **Interactive Terminal UI**: Replaced the previous dashboard with a multi-panel, command-driven terminal interface, including a `Ctrl+K` command palette.
-   **Modular Backend API**: Refactored the FastAPI backend to use a dynamic, "application-based" API with `/invoke/{app_name}` and `/ai-query` endpoints.
-   **Core Terminal Applications**: Implemented the `/news` and `/FA` (Fundamental Analysis) applications.
-   **Backend Testing**: Added a suite of `pytest` tests for the core backend API endpoints and AI orchestrator logic.
-   **Comprehensive Documentation**:
    -   Created `docs/philosophy.md` and `docs/architecture.md` to reflect the new AI-first vision.
    -   Added a `CONTRIBUTING.md` guide for future developers.
    -   Created a `CODE_OF_CONDUCT.md` to foster a professional community.
    -   Created `docs/limitations.md` to transparently outline the system's current capabilities.
-   **Definitive Dependencies**: Generated a complete `requirements.txt` file.

### Changed
-   **Project Vision**: Pivoted from a simple, non-predictive dashboard to a sophisticated, AI-driven, dual-mode system (autonomous agent + interactive terminal).
-   **Core Philosophy**: Moved from a "risk-first, non-predictive" model to an "AI-first, reality-first" model.

### Removed
-   **Old Dashboard UI**: The previous tab-based dashboard (`Chart`, `Risk Management`, etc.) has been completely removed in favor of the new terminal interface.
-   **Old Monolithic API**: The `/api/v1/analysis` endpoint has been removed and replaced by the new modular API.
-   **Old `core/` and `risk/` directories**: The previous logic for market structure and risk has been removed to make way for the new component-based architecture.

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
