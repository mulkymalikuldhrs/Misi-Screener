# Contributing to MiSi Screener

First off, thank you for considering contributing to MiSi Screener. Every contribution helps us build a more powerful and robust open-source intelligence platform. This guide provides comprehensive instructions for contributing to the project, whether you are fixing a bug, adding a new feature, improving documentation, or enhancing existing functionality.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure Overview](#project-structure-overview)
- [How to Contribute](#how-to-contribute)
- [Adding a New Data Source Connector](#adding-a-new-data-source-connector)
- [Adding a New Terminal Application](#adding-a-new-terminal-application)
- [Adding a New Agent](#adding-a-new-agent)
- [Adding a New Analytical Component](#adding-a-new-analytical-component)
- [Adding a New Strategy](#adding-a-new-strategy)
- [Running Tests](#running-tests)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to mulkymalikuldhaher@email.com.

---

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git
- A code editor or IDE (VS Code, PyCharm, etc.)

### Step-by-Step Setup

1. **Fork and clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Misi-Screener.git
    cd Misi-Screener
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install all required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up API Keys:**
    The system requires API keys for the `news` and `FA` (Fundamental Analysis) applications. Please obtain your free keys and set them as environment variables:
    ```bash
    export NEWS_API_KEY='your_key_from_newsapi.org'
    export ALPHA_VANTAGE_API_KEY='your_key_from_alphavantage.co'
    ```
    For convenience, you may create a `.env` file in the project root (this file is excluded from version control via `.gitignore`).

5. **Verify the installation:**
    ```bash
    pytest
    python -m uvicorn dashboard.backend.main:app --reload
    ```
    Open your browser to `http://127.0.0.1:8000` to confirm the dashboard loads correctly.

---

## Project Structure Overview

Understanding the project structure is essential for effective contributions:

```
Misi-Screener/
├── strategies/           # YAML-based strategy definitions
├── agents/               # AI agents for signal generation, portfolio management, etc.
├── components/           # Analytical modules and scoring engines
├── execution/            # Paper trading broker
├── data_sources/         # External data API connectors
├── dashboard/            # Web terminal (backend + frontend)
├── tests/                # Unit and integration tests
├── docs/                 # Project documentation
├── main.py               # Main entry point
├── run_backtest.py       # Backtesting CLI tool
└── requirements.txt      # Python dependencies
```

Each directory has a specific purpose and conventions. Please familiarize yourself with the existing code patterns before making contributions.

---

## How to Contribute

We welcome contributions in several forms:

- **Bug fixes**: Fix issues reported in the GitHub Issues tracker
- **New data source connectors**: Add support for additional market data APIs
- **New terminal applications**: Add new commands and visualizations to the dashboard
- **New agents**: Create specialized agents for novel analytical approaches
- **New analytical components**: Build new scoring or analysis engines
- **New strategies**: Define and share profitable trading strategies via YAML
- **Documentation improvements**: Fix typos, add examples, improve clarity
- **Performance optimizations**: Improve the speed or efficiency of existing code
- **Test coverage**: Add tests for untested code paths

### Contribution Workflow

1. **Check existing issues** or create a new one describing your proposed change
2. **Fork the repository** and create a feature branch from `feat/initial-project-structure`
3. **Make your changes** following the coding standards below
4. **Add tests** for any new functionality
5. **Ensure all tests pass** by running `pytest`
6. **Commit your changes** with a descriptive commit message
7. **Submit a pull request** with a clear description of the changes

---

## Adding a New Data Source Connector

Data source connectors provide the platform with real-time and historical market data. To add a new connector:

1. **Create the Connector File**: Add a new Python file in the `data_sources/` directory (e.g., `fred_connector.py`).

2. **Implement the Connector Class**: Inside the file, create a class that encapsulates the logic for fetching data from the new API. Follow the existing examples (`yfinance_connector.py`, `news_connector.py`, `alpha_vantage_connector.py`). The class should include:
    - An `__init__` method that sets up the API client and loads any required configuration
    - Public methods that correspond to the data endpoints you want to expose
    - Proper error handling and data validation

3. **Handle API Keys**: Ensure API keys are loaded from environment variables, not hardcoded. Use the pattern:
    ```python
    import os
    api_key = os.environ.get('YOUR_API_KEY_ENV_VAR')
    if not api_key:
        raise ValueError("YOUR_API_KEY_ENV_VAR environment variable is not set.")
    ```

4. **Add Dependencies**: If the connector requires new Python packages, add them to `requirements.txt` with pinned versions.

5. **Write Tests**: Add tests in the `tests/` directory to verify the connector's functionality.

---

## Adding a New Terminal Application

Terminal applications are the user-facing commands accessible through the dashboard:

1. **Register the App in the Backend**:
    - Import your new connector in `dashboard/backend/main.py`.
    - Instantiate it alongside the other services.
    - Add a new entry to the `APP_REGISTRY` dictionary. The key should be the function name (e.g., `get_economic_data`), and the value should be the method from your connector instance.

2. **Add the Command to the Frontend**:
    - Open `dashboard/frontend/index.html`.
    - Add a new entry to the `APPS` array in the JavaScript section. Define the `command` (e.g., `/econ`), a `description`, and the `app_name` (which must match the key in the `APP_REGISTRY`).

3. **Implement the Frontend Renderer**:
    - Open the `renderSingleAsset` function in the JavaScript section. Add a new `else if` block for your `app_name`.
    - Write the logic to parse the JSON data returned by your connector and render it as HTML.
    - For complex visualizations (like charts), you can directly manipulate the DOM and initialize JavaScript libraries within the `container` element passed to the function. See the `get_historical_data` case for a live example of how to implement a TradingView chart.

---

## Adding a New Agent

Agents are the decision-making entities in the platform. To add a new agent:

1. **Create the Agent File**: Add a new Python file in the `agents/` directory (e.g., `volatility_agent.py`).

2. **Implement the Agent Class**: Define the agent with a clear, single responsibility. The class should have:
    - A descriptive name and docstring explaining its role
    - A well-defined interface that other agents can consume
    - Proper error handling and logging

3. **Integrate with the Master Agent**: If the new agent should participate in the trading loop, update `agents/master_agent.py` to include it in the orchestration logic.

4. **Add Configuration Support**: If the agent has configurable parameters, add them to the strategy YAML schema and ensure they are properly loaded.

5. **Write Tests**: Add comprehensive tests in `tests/` for the new agent's core functionality.

---

## Adding a New Analytical Component

Components are specialized analytical engines that feed into the agent layer:

1. **Create the Component Directory**: Add a new directory in `components/` (e.g., `volatility_analysis/`).

2. **Implement the Engine**: Create an `engine.py` file inside the directory with the analytical logic. Follow the existing pattern (e.g., `components/quant_scoring/engine.py`).

3. **Define Clear Interfaces**: The component should accept well-defined inputs and produce structured outputs that agents can consume.

4. **Integrate with Agents**: Update the relevant agents to use the new component's output in their decision-making process.

5. **Write Tests**: Add tests in `tests/components/` for the component's core calculations and edge cases.

---

## Adding a New Strategy

Strategies are defined in YAML and require no Python code changes:

1. **Study existing strategies**: Review `strategies/mean_reversion_rsi.yml` for the expected format.

2. **Create your strategy YAML**: Define the strategy with the following sections:
    - `name`: A descriptive name for the strategy
    - `asset_ticker`: The target asset (e.g., `AAPL`, `BTC-USD`)
    - `entry_conditions`: The conditions that trigger a BUY signal
    - `exit_conditions`: The conditions that trigger a SELL signal
    - `risk_management`: Parameters including stop-loss method, risk per trade percentage, etc.

3. **Backtest thoroughly**: Always validate your strategy using the backtesting engine before considering it for live trading:
    ```bash
    python run_backtest.py strategies/your_strategy.yml --start "2022-01-01" --end "2024-01-01"
    ```

4. **Document the strategy**: Add a comment block at the top of the YAML file explaining the strategy's logic, expected market conditions, and known limitations.

---

## Running Tests

Before submitting a contribution, please ensure that all existing tests pass and, if possible, add new tests for your functionality.

### Run the full test suite:
```bash
pytest
```

### Run a specific test file:
```bash
pytest tests/test_backend_api.py
```

### Run with verbose output:
```bash
pytest -v
```

### Run with coverage reporting:
```bash
pytest --cov=. --cov-report=term-missing
```

All new code contributions should include corresponding test coverage. Aim for at least 80% coverage on new code.

---

## Coding Standards

### Python Style

- Follow the **PEP 8** style guide for Python code. Use a linter like `flake8` or `ruff` to enforce consistency.
- Use **type hints** for function signatures and return types. This improves code readability and enables better IDE support.
- Keep functions **small and focused**. Each function should do one thing well.
- Use **descriptive variable and function names**. Avoid single-letter variables except in mathematical contexts.
- Add **docstrings** to all public classes, methods, and functions following the Google or NumPy style.

### Code Quality

- Keep code clean, well-commented, and modular.
- Ensure that user-facing text (in the UI or in logs) is clear and informative.
- Avoid code duplication. If you find yourself copying and pasting code, consider extracting it into a shared utility function.
- Handle errors gracefully with informative error messages. Never silently swallow exceptions.

### Import Organization

Organize imports in the following order:
1. Standard library imports
2. Third-party library imports
3. Local application imports

Separate each group with a blank line.

---

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Examples

```
feat(agents): add volatility analysis agent
fix(backtest): correct lookahead bias in historical data fetch
docs(readme): update installation instructions
test(backend): add tests for portfolio manager position sizing
```

---

## Pull Request Process

1. **Update documentation**: Ensure that any new features or changed behavior are reflected in the relevant documentation files.

2. **Add tests**: All new functionality must include appropriate test coverage. Bug fixes should include a test that verifies the fix.

3. **Ensure CI passes**: All tests must pass before a pull request can be merged.

4. **Write a clear PR description**: Include:
    - What the change does and why it is needed
    - How to test the change
    - Any breaking changes or migration steps
    - Links to related issues

5. **Request review**: At least one maintainer must approve the pull request before it can be merged.

6. **Keep PRs focused**: Each pull request should address a single concern. Large, multi-purpose PRs are harder to review and slower to merge.

---

## Reporting Issues

When reporting bugs or requesting features, please use the GitHub Issues tracker and include:

- **For bugs**: A clear description of the issue, steps to reproduce, expected behavior, actual behavior, and your environment (Python version, OS, etc.)
- **For features**: A clear description of the proposed feature, the use case it addresses, and any alternative solutions you have considered.

---

## Community

- GitHub: [https://github.com/mulkymalikuldhrs/Misi-Screener](https://github.com/mulkymalikuldhrs/Misi-Screener)
- Related Project: [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS)
- Maintainer: Mulky Malikul Dhaher (mulkymalikuldhaher@email.com)

Thank you for helping to make MiSi Screener a world-class tool. Your contributions, no matter how small, are valued and appreciated.
