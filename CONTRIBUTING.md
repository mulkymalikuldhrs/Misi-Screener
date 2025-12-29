# Contributing to MiSi Screener: The AI Quant Trading System

We are thrilled that you're interested in contributing to MiSi Screener! We are on a mission to build the world's most advanced open-source, AI-driven trading system, and we need the brightest minds in the community to help us achieve this vision.

## Our Core Vision

Before contributing, please read our new project philosophy and architecture to understand our goals:

1.  **[Our AI-Driven Philosophy (`docs/philosophy.md`)](./docs/philosophy.md):** Understand our goal to build an autonomous system that surpasses human trading capabilities.
2.  **[Our Multi-Agent Architecture (`docs/architecture.md`)](./docs/architecture.md):** Understand the roles of the different AI agents and how they collaborate.

**We welcome contributions that push the boundaries of AI in finance.**

## How to Contribute

1.  **Find an Issue or Propose an Idea:** Check our [Issues tab](https://github.com/mulkymalikuldhrs/Misi-Screener/issues) or our `TODO.md` file for areas where you can help. If you have a new idea, please open an issue to discuss it first.
2.  **Fork the Repository:** Create your own copy of the project to work on.
3.  **Create a Branch:** Create a descriptive branch for your feature or bugfix (e.g., `feat/add-bollinger-bands` or `fix/risk-manager-logic`).
4.  **Write High-Quality Code:** Implement your changes, following best practices.
5.  **Add Tests:** All new logic, especially in the `components/` library, must be accompanied by deterministic unit tests.
6.  **Update Documentation:** If you add a new agent, feature, or change the architecture, please update the relevant documentation.
7.  **Submit a Pull Request:** Open a PR and provide a clear description of your changes.

## Types of Contributions We're Looking For

-   **New Technical Indicators:** Add new functions to `components/technical_indicators.py` (and don't forget the tests!).
-   **New Trading Strategies:** Add new strategy files to the `strategies/` directory.
-   **Improving Agent Logic:** Propose improvements to the "thinking" process of our AI agents.
-   **Data Source Connectors:** Build new modules in `data_sources/` to connect to more market, fundamental, or sentiment data APIs.
-   **Dashboard Development:** Help us design and build a stunning and intuitive frontend in the `dashboard/` directory.
-   **Bug Fixes & Performance Improvements:** Help us make the system faster, more robust, and more reliable.

Thank you for being a part of this ambitious journey!
