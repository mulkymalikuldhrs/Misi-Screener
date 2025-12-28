# Contributing to MiSi Screener

We welcome contributions to MiSi Screener. However, this project is governed by a strict development philosophy. Before contributing, you must read and agree to our core principles.

## Core Philosophy

Please read and internalize the following documents before writing any code:

1.  **[Our Philosophy (`docs/philosophy.md`)](./docs/philosophy.md):** Understand that this is a non-predictive, risk-first system.
2.  **[Our Architecture (`docs/architecture.md`)](./docs/architecture.md):** Understand the role of each module and the absolute authority of the Risk Governor.
3.  **[Our Limitations (`docs/limitations.md`)](./docs/limitations.md):** Understand when and why the system is designed to fail or refuse analysis.
4.  **[Our Validation Framework (`docs/validation.md`)](./docs/validation.md):** Understand that we do not use backtesting.

**Any pull request that violates these core principles will be rejected.**

## How to Contribute

1.  **Open an Issue:** Before starting work on a new feature or bugfix, please open an issue to discuss it with the maintainers. This ensures that your work is aligned with the project's roadmap and goals.
2.  **Fork the Repository:** Create a fork of the repository to your own GitHub account.
3.  **Create a Branch:** Create a new branch for your feature or bugfix.
4.  **Write Code:** Write your code, ensuring it adheres to the project's coding standards and architectural principles.
5.  **Add Tests:** All new features must be accompanied by unit tests.
6.  **Update Documentation:** If your changes affect the system's behavior or architecture, you must update the relevant documentation.
7.  **Submit a Pull Request:** Open a pull request from your fork to the main repository. Provide a clear description of your changes and link to the relevant issue.

## Prohibited Contributions

The following types of contributions will be rejected immediately:

-   Any feature that introduces predictive capabilities (e.g., price forecasting, signal generation).
-   Any change that attempts to optimize for PnL or other performance metrics.
-   Any validation method based on backtesting or historical simulation.
-   Any UI change that adds emotionally charged or "gamified" elements.
-   Any change that allows the Risk Governor to be overridden by a user or another module.

We are building a tool for serious risk management, not a signal-generation engine. Thank you for your understanding and cooperation.
