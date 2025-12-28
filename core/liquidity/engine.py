"""
This file contains the core logic for the Liquidity & Participation Engine.

Designed from a 'first-principles' approach, this engine is purely
deterministic and non-predictive. It aims to provide an objective measure of
market activity and pressure without relying on broker-specific data or
complex, non-auditable models.
"""

from dataclasses import dataclass
import pandas as pd
import numpy as np

# --- 1. Core Data Structures ---

@dataclass(frozen=True)
class LiquiditySweep:
    """
    Represents a single detected liquidity sweep event.
    """
    timestamp: pd.Timestamp
    price_level: float
    is_high_sweep: bool # True if it's a sweep of a high, False for a low

@dataclass(frozen=True)
class LiquidityOutput:
    """
    The final output of the Liquidity & Participation Engine.
    """
    participation_score: pd.Series # A score (0-100) for each candle
    liquidity_sweeps: list[LiquiditySweep] # A list of detected sweep events

# --- 2. The Liquidity & Participation Engine ---

class LiquidityEngine:
    """
    A stateless engine that takes price data and returns a measure of
    liquidity and participation.
    """

    def analyze_liquidity(self, ohlc_data: pd.DataFrame, participation_period: int, sweep_lookback: int) -> LiquidityOutput:
        """
        Analyzes the provided OHLC data to calculate a participation score and
        detect liquidity sweeps.

        Args:
            ohlc_data: A pandas DataFrame with ['timestamp', 'high', 'low', 'close', 'volume'].
            participation_period: The lookback period for calculating the participation score.
            sweep_lookback: The number of bars to look back to identify a high/low for a potential sweep.

        Returns:
            A LiquidityOutput object containing the analysis.
        """

        # --- Participation Score Logic (First Principles) ---
        true_range = ohlc_data['high'] - ohlc_data['low']
        volume_rank = ohlc_data['volume'].rolling(window=participation_period).apply(lambda x: x.rank(pct=True).iloc[-1], raw=False)
        range_rank = true_range.rolling(window=participation_period).apply(lambda x: x.rank(pct=True).iloc[-1], raw=False)
        participation_score = (volume_rank * 0.6 + range_rank * 0.4) * 100
        participation_score = participation_score.fillna(0)


        # --- Liquidity Sweep Logic (Corrected First Principles) ---
        # A liquidity sweep occurs when price breaks a recent high/low but
        # fails to continue, closing back within the previous range.

        sweeps = []
        # Vectorized approach for clarity and performance
        prev_highs = ohlc_data['high'].shift(1).rolling(window=sweep_lookback).max()
        prev_lows = ohlc_data['low'].shift(1).rolling(window=sweep_lookback).min()

        high_sweep_candidates = (ohlc_data['high'] > prev_highs) & (ohlc_data['close'] < prev_highs)
        low_sweep_candidates = (ohlc_data['low'] < prev_lows) & (ohlc_data['close'] > prev_lows)

        for i in ohlc_data[high_sweep_candidates].index:
            sweeps.append(LiquiditySweep(
                timestamp=ohlc_data['timestamp'].loc[i],
                price_level=prev_highs.loc[i],
                is_high_sweep=True
            ))

        for i in ohlc_data[low_sweep_candidates].index:
            sweeps.append(LiquiditySweep(
                timestamp=ohlc_data['timestamp'].loc[i],
                price_level=prev_lows.loc[i],
                is_high_sweep=False
            ))


        return LiquidityOutput(
            participation_score=participation_score,
            liquidity_sweeps=sweeps
        )
