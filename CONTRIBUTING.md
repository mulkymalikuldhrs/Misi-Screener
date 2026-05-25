# Contributing to MiSi Screener

First off, thank you for considering contributing to MiSi Screener. Every contribution helps us build a more powerful and robust open-source intelligence platform.

This document provides guidelines for contributing to the project.

## Development Environment Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
    cd Misi-Screener
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install all required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Keys:**
    The system requires API keys for the `news` and `FA` (Fundamental Analysis) applications. Please obtain your free keys and set them as environment variables:
    ```bash
    export NEWS_API_KEY='your_key_from_newsapi.org'
    export ALPHA_VANTAGE_API_KEY='your_key_from_alphavantage.co'
    ```

5.  **Run the application:**
    To run the interactive terminal, start the backend server from the **project root directory**:
    ```bash
    python -m uvicorn dashboard.backend.main:app --reload
    ```

## How to Contribute

We welcome contributions in several forms, primarily by adding new Data Source Connectors and Terminal Applications.

### Adding a New Data Source Connector

1.  **Create the Connector File**: Add a new Python file in the `data_sources/` directory (e.g., `my_api_connector.py`).
2.  **Implement the Connector Class**: Inside the file, create a class that encapsulates the logic for fetching data from the new API. Follow the existing examples (`yfinance_connector.py`, `news_connector.py`).
3.  **Handle API Keys**: Ensure API keys are loaded from environment variables, not hardcoded.

### Adding a New Terminal Application

1.  **Register the App in the Backend**:
    *   Import your new connector in `dashboard/backend/main.py`.
    *   Instantiate it with the other services.
    *   Add a new entry to the `APP_REGISTRY` dictionary. The key should be the function name (e.g., `get_economic_data`), and the value should be the method from your connector instance.

2.  **Add the Command to the Frontend**:
    *   Open `dashboard/frontend/index.html`.
    *   Add a new entry to the `APPS` array in the JavaScript section. Define the `command` (e.g., `/econ`), a `description`, and the `app_name` (which must match the key in the `APP_REGISTRY`).

3.  **Implement the Frontend Renderer**:
    *   Open the `renderSingleAsset` function in the JavaScript section. Add a new `else if` block for your `app_name`.
    *   Write the logic to parse the JSON data returned by your connector and render it as HTML.
    *   **For complex visualizations (like charts)**, you can directly manipulate the DOM and initialize JavaScript libraries within the `container` element passed to the function. See the `get_historical_data` case for a live example of how to implement a TradingView chart.

## Running Tests

Before submitting a contribution, please ensure that all existing tests pass and, if possible, add new tests for your functionality.

1.  **Run the test suite:**
    ```bash
    pytest
    ```

## Coding Style

-   Please follow the **PEP 8** style guide for Python code.
-   Keep code clean, commented, and modular.
-   Ensure that user-facing text (in the UI or in logs) is clear and informative.

Thank you for helping to make MiSi Screener a world-class tool!

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
