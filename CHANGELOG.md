# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-AI-Vision] - 2024-05-22

### Changed

-   **MAJOR PIVOT: Project Re-founded as an Autonomous AI Trading System.**
    -   The project's original philosophy of being a non-predictive, deterministic, decision-support tool has been **completely deprecated**.
    -   `MiSi Screener` is now an ambitious open-source project to build a fully autonomous, AI-driven quantitative trading system.

-   **Complete Architectural Overhaul:**
    -   Removed the old `core`, `data`, and `tests` directories, which were based on the deterministic model.
    -   Created a new, agent-centric architecture with the following directories: `agents`, `strategies`, `data_sources`, `components`, and `dashboard`.
    -   Added a new `main.py` entry point to orchestrate the AI agent collective.

-   **Documentation Rewrite:**
    -   Overhauled `README.md` to reflect the new vision, project goals, and a strong call for collaborators.
    -   Rewrote `docs/philosophy.md` to detail the new AI-centric, autonomous, and predictive philosophy.
    -   Rewrote `docs/architecture.md` to describe the new multi-agent system framework.
    -   Added official project lead and contact information.

## [0.1.0] - 2024-05-22 [DEPRECATED]

### This version is now deprecated and has been replaced by the new AI-driven vision.

-   **Initial Project Scaffolding:**
    -   Created the directory structure for a deterministic, non-predictive system.
    -   Established foundational documentation for the non-predictive philosophy.
-   **Core Engines (Deterministic):**
    -   Implemented and tested the `MarketStructureEngine`, `LiquidityEngine`, `RegimeEngine`, and `RiskGovernor`.
-   **Repository Hygiene:**
    -   Added `.gitignore`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.
