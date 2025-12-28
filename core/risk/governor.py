"""
This file contains the logic for the Risk Governor, the ultimate authority
in the MiSi Screener system.
"""

from enum import Enum, auto
from dataclasses import dataclass

# --- 1. Define the Core States and Data Structures ---

class PermissionState(Enum):
    """
    Defines the three possible states the Risk Governor can be in.
    This is the highest-level directive.
    """
    BLOCK = auto()      # All analytical modules are disabled. No context is generated.
    RESTRICT = auto()   # Analysis is permitted, but with strict limitations.
    ALLOW = auto()      # Analysis is permitted under normal parameters.


@dataclass(frozen=True)
class RiskInput:
    """
    A snapshot of all risk-related metrics required by the governor.
    This object is the sole input for the governor's decision.
    """
    # Volatility Metrics
    realized_volatility: float  # e.g., 30-day realized vol
    volatility_percentile: float # Realized vol's percentile over a long lookback (0.0 to 1.0)

    # Regime Context (from the Regime Engine)
    current_regime: str         # e.g., "Compression", "Stress", "Expansion"
    regime_confidence: float    # How strongly the data fits the regime (0.0 to 1.0)

    # Drawdown Metrics
    system_drawdown: float      # Current drawdown of the system/portfolio (0.0 to 1.0)
    is_new_equity_high: bool    # Is the underlying portfolio at a new equity high?

    # Data Quality Metrics (from the Data Pipeline)
    data_integrity_score: float # Score of the current data quality (0.0 to 1.0)


@dataclass(frozen=True)
class GovernorDirective:
    """
    The final output of the Risk Governor.
    This is the set of rules that all other modules must obey.
    """
    permission_state: PermissionState
    reason: str
    # Future potential restrictions
    # max_allowed_timeframe: str = "H4"
    # max_analysis_frequency_hz: int = 1


# --- 2. The Risk Governor Class ---

class RiskGovernor:
    """
    The central authority for risk assessment. It is a stateless class that
    translates a RiskInput object into a GovernorDirective.
    """

    def assess_risk(self, inputs: RiskInput) -> GovernorDirective:
        """
        The core decision-making function. It evaluates the risk inputs
        based on a cascading set of rules, from most severe to least severe.

        The first rule that triggers a BLOCK or RESTRICT state returns
        immediately. The default state is ALLOW.
        """

        # --- RULE 1: DATA INTEGRITY (Absolute Priority) ---
        # If data quality is compromised, nothing else matters.
        if inputs.data_integrity_score < 0.8:
            return GovernorDirective(
                permission_state=PermissionState.BLOCK,
                reason="Critical data integrity failure."
            )

        # --- RULE 2: EXTREME MARKET STRESS ---
        # The "Stress / Breakdown" regime is a non-discretionary BLOCK.
        if inputs.current_regime == "Stress / Breakdown":
            return GovernorDirective(
                permission_state=PermissionState.BLOCK,
                reason="Market regime is 'Stress / Breakdown'. Analysis is suspended."
            )

        # --- RULE 3: EXTREME VOLATILITY ---
        # If volatility is in the top percentile (e.g., > 95th), conditions are
        # too unstable for most analysis.
        if inputs.volatility_percentile > 0.95:
            return GovernorDirective(
                permission_state=PermissionState.BLOCK,
                reason=f"Extreme volatility detected (Percentile: {inputs.volatility_percentile:.2f})."
            )

        # --- RULE 4: SEVERE DRAWDOWN ---
        # If the system is in a significant drawdown, tighten risk aggressively.
        if inputs.system_drawdown > 0.20: # Example: 20% drawdown
            return GovernorDirective(
                permission_state=PermissionState.BLOCK,
                reason=f"Severe system drawdown detected ({inputs.system_drawdown:.2f})."
            )

        # --- RULE 5: HIGH VOLATILITY + DRAWDOWN (Restriction) ---
        # If volatility is high (but not extreme) AND the system is in a drawdown,
        # restrict activity but don't block it entirely. This is a critical
        # "defensive mode".
        if inputs.volatility_percentile > 0.80 and inputs.system_drawdown > 0.10:
             return GovernorDirective(
                permission_state=PermissionState.RESTRICT,
                reason=(f"High volatility (P:{inputs.volatility_percentile:.2f}) "
                        f"coinciding with system drawdown (DD:{inputs.system_drawdown:.2f}).")
            )

        # --- RULE 6: LOW REGIME CONFIDENCE (Restriction) ---
        # If the market is choppy and the Regime Engine is not confident in its
        # classification, it's prudent to be cautious.
        if inputs.regime_confidence < 0.6:
            return GovernorDirective(
                permission_state=PermissionState.RESTRICT,
                reason=f"Low regime confidence ({inputs.regime_confidence:.2f}). Market is unclear."
            )

        # --- DEFAULT STATE: ALLOW ---
        # If no blocking or restricting rules were triggered, the system is
        # cleared for normal operation. We still provide a reason for clarity.
        reason = "Conditions are within normal operating parameters."
        if inputs.is_new_equity_high:
            reason = "System at new equity high; conditions normal."

        return GovernorDirective(
            permission_state=PermissionState.ALLOW,
            reason=reason
        )

# --- Example Usage (for demonstration) ---
#
# if __name__ == '__main__':
#     governor = RiskGovernor()
#
#     # Example 1: Catastrophic event
#     bad_inputs = RiskInput(
#         realized_volatility=0.8,
#         volatility_percentile=0.99,
#         current_regime="Stress / Breakdown",
#         regime_confidence=0.9,
#         system_drawdown=0.25,
#         is_new_equity_high=False,
#         data_integrity_score=0.95
#     )
#     directive = governor.assess_risk(bad_inputs)
#     # Expected: BLOCK due to regime
#     print(f"Directive: {directive.permission_state}, Reason: {directive.reason}")
#
#     # Example 2: Defensive mode
#     defensive_inputs = RiskInput(
#         realized_volatility=0.4,
#         volatility_percentile=0.85,
#         current_regime="Expansion",
#         regime_confidence=0.8,
#         system_drawdown=0.12,
#         is_new_equity_high=False,
#         data_integrity_score=0.99
#     )
#     directive = governor.assess_risk(defensive_inputs)
#     # Expected: RESTRICT due to vol + drawdown
#     print(f"Directive: {directive.permission_state}, Reason: {directive.reason}")
#
#     # Example 3: Normal conditions
#     good_inputs = RiskInput(
#         realized_volatility=0.2,
#         volatility_percentile=0.5,
#         current_regime="Compression",
#         regime_confidence=0.9,
#         system_drawdown=0.05,
#         is_new_equity_high=True,
#         data_integrity_score=1.0
#     )
#     directive = governor.assess_risk(good_inputs)
#     # Expected: ALLOW
#     print(f"Directive: {directive.permission_state}, Reason: {directive.reason}")
