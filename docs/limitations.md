# Limitations

This document outlines the known limitations of the MiSi Screener system. It is critical for all users and developers to understand these boundaries to use the system responsibly.

## 1. Not a Predictive System

- **MiSi Screener is not a forecasting tool.** It does not and will not provide price targets, entry/exit signals, or any form of market prediction. Its sole purpose is to provide a structured, data-driven assessment of the *current* market context. Misinterpreting its output as a predictive signal is a serious misuse of the system.

## 2. Dependence on Data Quality

- **The system's output is only as good as its input data.** The `data/` pipeline includes integrity checks, but it cannot defend against all possible data issues. Gaps, errors, or low-quality data in the OHLCV feed will lead to unreliable analysis. In such cases, the system is designed to refuse analysis rather than provide a flawed output.

## 3. No Guarantee of Performance

- **The analysis provided by MiSi Screener does not guarantee any specific trading outcome.** It is a decision-support tool, not a trading strategy. The user is solely responsible for how they interpret and act upon the information provided.

## 4. Discretion is Required

- **The system is a tool for augmenting, not replacing, human discretion.** It provides a quantitative view of the market but does not understand all market dynamics, news events, or nuanced contextual factors. Users must apply their own judgment and experience.

## 5. Lagging by Nature

- **All calculations are based on historical price data.** Therefore, the system's outputs are, by definition, lagging indicators of market conditions. They describe the recent past, not the future.

## When the System Will Reject the User

The system is explicitly designed to refuse to provide analysis under certain conditions. This is a feature, not a bug. Expect the system to return a "BLOCK" or "REFUSE" status when:

- **Input data fails integrity checks.** If the data is incomplete, noisy, or otherwise unsuitable, the system will not proceed.
- **The Risk Governor detects extreme conditions.** During periods of extreme volatility, high systemic drawdown, or stressed correlations, the Risk Governor has the authority to block all other analytical outputs.
- **The current market regime is incompatible with a requested analysis.** For example, the system will refuse to validate a breakout setup during a clear `Compression` regime.

The system is designed to say "I don't know" or "No" far more often than it provides actionable context. This is core to its risk-first philosophy.
