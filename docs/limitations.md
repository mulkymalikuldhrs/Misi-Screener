# Limitations

This document outlines the known limitations of the MiSi Screener system. It is critical for all users and developers to understand these boundaries to use the system responsibly.

## 1. Not a Predictive System

- **MiSi Screener is not a forecasting tool.** It does not and will not provide price targets, entry/exit signals, or any form of market prediction. Its sole purpose is to provide a structured, data-driven assessment of the *current* market context. Misinterpreting its output as a predictive signal is a serious misuse of the system.

## 2. Dependence on Data Quality

- **The system's output is only as good as its input data.** While the `data/validators` module is designed to catch common issues, it cannot protect against all forms of data corruption or anomaly. Gaps, errors, or low-quality data in the OHLCV feed will lead to unreliable and potentially misleading analysis.

## 3. No Guarantee of Performance

- **The analysis provided by MiSi Screener does not guarantee any specific trading outcome.** It is a decision-support tool, not a strategy. The user is solely responsible for how they interpret and act upon the information provided.

## 4. Discretion is Required

- **The system is a tool for augmenting, not replacing, human discretion.** It provides a quantitative view of the market, but it does not understand all market dynamics, news events, or nuanced contextual factors. Users must apply their own judgment and experience.

## 5. Lagging by Nature

- **All calculations are based on historical price data.** Therefore, the system's outputs are, by definition, lagging indicators of market conditions. They describe the recent past, not the future.
