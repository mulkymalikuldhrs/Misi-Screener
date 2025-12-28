# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-05-22

### Added

- **Initial Project Scaffolding:**
    - Created the complete, production-ready directory structure for `core`, `data`, `api`, `frontend`, `docs`, and `tests`.
    - Established foundational documentation including `philosophy.md`, `architecture.md`, `limitations.md`, and `references.md` which lock in the project's non-predictive, risk-first principles.
- **Market Structure Engine (`core/structure`):**
    - Implemented a deterministic, "first-principles" `MarketStructureEngine` for swing detection.
    - Added a comprehensive unit test suite (`tests/core/structure/test_engine.py`) to ensure deterministic behavior and correctness.
- **Risk Governor (`core/risk`):**
    - Implemented the `RiskGovernor`, the system's ultimate authority, with a clear, cascading set of rules for issuing `ALLOW`, `RESTRICT`, and `BLOCK` directives.
    - Added a full suite of unit tests (`tests/core/risk/test_governor.py`) to validate every rule and priority level, ensuring the system's central safety mechanism is reliable.
- **Repository Hygiene:**
    - Added a `.gitignore` file to prevent committing of build artifacts, cache files, and IDE configurations.
- **Validation Framework:**
    - Created `docs/validation.md` to formally forbid backtesting and establish forward-observation and failure-logging as the only approved validation methods.
- **Contribution Guidelines:**
    - Added `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` to establish clear and safe guidelines for open-source collaboration.

## [Unreleased]

- Future development will be documented here.
