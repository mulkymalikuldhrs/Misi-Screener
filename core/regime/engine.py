"""
This file contains the core logic for the Regime Classification Engine.

This engine synthesizes inputs from the Structure and Liquidity engines, along
with its own volatility analysis, to classify the market's current behavioral
state. The logic is deterministic and rule-based, adhering to the project's
non-predictive philosophy.
"""

from dataclasses import dataclass
from enum import Enum, auto
import pandas as pd
import numpy as np

# --- 1. Core Data Structures ---

class Regime(Enum):
    """The five finalized, non-negotiable market regimes."""
    EXPANSION = auto()
    COMPRESSION = auto()
    TRANSITION = auto()
    MEAN_REVERSION = auto()
    STRESS_BREAKDOWN = auto()

@dataclass(frozen=True)
class RegimeInput:
    """
    Represents the combined inputs required for regime classification.
    These are derived from the OHLCV data and the outputs of other engines.
    """
    atr_percentile: float         # Volatility (0.0 to 1.0)
    structure_stability: float    # Structure (0.0 to 1.0, 1.0 is a clear trend)
    participation_score: float    # Liquidity (0 to 100)

@dataclass(frozen=True)
class RegimeOutput:
    """
    The final output of the Regime Engine for a single point in time.
    """
    regime: Regime
    confidence: float # How clearly the inputs match the regime's profile (0.0 to 1.0)
    incompatible_actions: list[str] # A list of logic types invalid in this regime

# --- 2. The Regime Engine ---

class RegimeEngine:
    """
    A stateless engine that classifies the market regime based on a set of
    quantitative inputs.
    """

    def classify_regime(self, inputs: RegimeInput) -> RegimeOutput:
        """
        Classifies the market regime using a deterministic, rule-based approach.

        The logic checks for the most extreme conditions first (Stress) and then
        works down to the most common (Expansion/Compression).

        Args:
            inputs: A RegimeInput object containing the latest market metrics.

        Returns:
            A RegimeOutput object with the classified regime and associated metadata.
        """

        # --- Rule 1: STRESS / BREAKDOWN ---
        # Characterized by extreme volatility and a complete breakdown of structure.
        if inputs.atr_percentile > 0.95 and inputs.structure_stability < 0.2:
            return RegimeOutput(
                regime=Regime.STRESS_BREAKDOWN,
                confidence=min(inputs.atr_percentile, (1 - inputs.structure_stability)),
                incompatible_actions=["trend_following", "mean_reversion", "breakout"]
            )

        # --- Rule 2: COMPRESSION ---
        # Characterized by very low volatility and low participation. Structure is irrelevant.
        if inputs.atr_percentile < 0.2 and inputs.participation_score < 30:
            return RegimeOutput(
                regime=Regime.COMPRESSION,
                confidence= (1 - inputs.atr_percentile) * (1 - inputs.participation_score / 100),
                incompatible_actions=["trend_following", "breakout"]
            )

        # --- Rule 3: EXPANSION ---
        # Characterized by high volatility, high participation, and clear structure.
        if inputs.atr_percentile > 0.7 and inputs.participation_score > 70 and inputs.structure_stability > 0.6:
            return RegimeOutput(
                regime=Regime.EXPANSION,
                confidence=np.mean([inputs.atr_percentile, inputs.participation_score / 100, inputs.structure_stability]),
                incompatible_actions=["mean_reversion"]
            )

        # --- Rule 4: MEAN REVERSION ---
        # Characterized by medium-high volatility but a distinct LACK of structure (choppy).
        if inputs.atr_percentile > 0.6 and inputs.structure_stability < 0.4:
            return RegimeOutput(
                regime=Regime.MEAN_REVERSION,
                confidence=np.mean([inputs.atr_percentile, (1 - inputs.structure_stability)]),
                incompatible_actions=["trend_following", "breakout"]
            )

        # --- Default Rule: TRANSITION ---
        # If none of the specific regimes are met, the market is in a state of transition.
        return RegimeOutput(
            regime=Regime.TRANSITION,
            confidence=0.5, # Confidence is neutral by definition
            incompatible_actions=[] # No actions are strictly incompatible, but none are ideal
        )
