# Current System Limitations

This document outlines the current limitations of the MiSi Screener system as of v1.0. While the foundational architecture is robust and scalable, it is important to be transparent about what is not yet implemented.

This serves as a roadmap for future development and helps manage user and contributor expectations.

### 1. AI Orchestrator is Rule-Based, Not a True LLM

-   **Limitation**: The `AdvancedQueryOrchestrator` is a significant step forward, but it is still a rule-based engine. It uses more sophisticated regular expressions and logic to parse intents and multiple entities, but it does not possess true natural language understanding (NLU).
-   **Impact**: It can now handle more complex queries like "news for AAPL and MSFT", but it cannot understand conversational context, follow-up questions, or queries with significant ambiguity. Performance will degrade on queries that do not follow a relatively clear "intent + entities" structure.
-   **Future Work**: The `AIAgent` is designed to be the integration point for a true Large Language Model (LLM). Future work will involve replacing the `AdvancedQueryOrchestrator` with a component that calls an LLM (e.g., via the OpenAI API, Hugging Face, or a local model) to parse queries, enabling far more flexible and powerful conversational analysis.

### 2. Dependency on Public API Keys and Rate Limits

-   **Limitation**: The system relies entirely on free, public APIs for all its data (`NewsAPI`, `Alpha Vantage`, etc.). These APIs have strict rate limits (e.g., a certain number of calls per minute or per day).
-   **Impact**: Heavy use of the terminal in a short period can temporarily exhaust the API keys, leading to data failing to load in the UI. There is currently no caching mechanism to mitigate this.
-   **Future Work**: A caching layer (e.g., using Redis) will be implemented to store recent API calls, reducing redundant fetches and making the system more resilient to rate limiting. Support for premium/paid API keys with higher limits could also be added.

### 3. No Data Persistence or User Management

-   **Limitation**: The terminal is stateless. There is no database, user accounts, or mechanism to save layouts, preferences, or analysis.
-   **Impact**: Every time the application is loaded, it starts with a blank slate.
-   **Future Work**: A database backend (e.g., PostgreSQL or SQLite) and a user authentication system will be added to enable persistent workspaces, saved queries, and personalized settings.

### 4. Limited Set of "Apps" and Connectors

-   **Limitation**: The initial release only includes connectors and applications for basic market data (`/chart`), news (`/news`), and company fundamentals (`/FA`).
-   **Impact**: A vast number of analytical domains are not yet covered, such as economic data, options chains, alternative data, social sentiment analysis, etc.
-   **Future Work**: The `data_sources` and `dashboard` modules are designed for easy extension. New connectors and terminal apps will be a primary focus of ongoing development.

### 5. No Autonomous Agent Capabilities

-   **Limitation**: While the architecture is designed to support them, there are currently no autonomous agents implemented. The system can only be used interactively through the terminal.
-   **Impact**: The "dual-mode" vision is not yet realized. The system cannot perform background monitoring, send alerts, or execute strategies on its own.
-   **Future Work**: Developing the first autonomous agents (e.g., `MarketScannerAgent`) is a key priority on the project roadmap.

---
> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
