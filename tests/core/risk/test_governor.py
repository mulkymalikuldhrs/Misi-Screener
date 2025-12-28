"""
Unit tests for the Risk Governor.
"""
import pytest
from core.risk.governor import RiskGovernor, RiskInput, PermissionState
from dataclasses import asdict

@pytest.fixture
def governor():
    """Provides a RiskGovernor instance."""
    return RiskGovernor()

@pytest.fixture
def base_input_dict():
    """Provides a default, low-risk input dictionary for tests to modify."""
    return asdict(RiskInput(
        realized_volatility=0.2,
        volatility_percentile=0.5,
        current_regime="Expansion",
        regime_confidence=0.9,
        system_drawdown=0.05,
        is_new_equity_high=False, # Default to False for the base case
        data_integrity_score=1.0
    ))

def test_rule_1_data_integrity_failure(governor, base_input_dict):
    """Test RULE 1: BLOCK on critical data integrity failure."""
    kwargs = base_input_dict.copy()
    kwargs['data_integrity_score'] = 0.79
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.BLOCK
    assert "data integrity failure" in directive.reason

def test_rule_2_market_stress_regime(governor, base_input_dict):
    """Test RULE 2: BLOCK on 'Stress / Breakdown' regime."""
    kwargs = base_input_dict.copy()
    kwargs['current_regime'] = "Stress / Breakdown"
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.BLOCK
    assert "Market regime is 'Stress / Breakdown'" in directive.reason

def test_rule_3_extreme_volatility(governor, base_input_dict):
    """Test RULE 3: BLOCK on extreme volatility."""
    kwargs = base_input_dict.copy()
    kwargs['volatility_percentile'] = 0.96
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.BLOCK
    assert "Extreme volatility detected" in directive.reason

def test_rule_4_severe_drawdown(governor, base_input_dict):
    """Test RULE 4: BLOCK on severe system drawdown."""
    kwargs = base_input_dict.copy()
    kwargs['system_drawdown'] = 0.21
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.BLOCK
    assert "Severe system drawdown detected" in directive.reason

def test_rule_5_high_vol_plus_drawdown(governor, base_input_dict):
    """Test RULE 5: RESTRICT on high volatility coinciding with drawdown."""
    kwargs = base_input_dict.copy()
    kwargs['volatility_percentile'] = 0.85
    kwargs['system_drawdown'] = 0.11
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.RESTRICT
    assert "High volatility" in directive.reason and "coinciding with system drawdown" in directive.reason

def test_rule_6_low_regime_confidence(governor, base_input_dict):
    """Test RULE 6: RESTRICT on low regime confidence."""
    kwargs = base_input_dict.copy()
    kwargs['regime_confidence'] = 0.59
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.RESTRICT
    assert "Low regime confidence" in directive.reason

def test_default_allow_state(governor, base_input_dict):
    """Test the default ALLOW state when no restrictive rules are met."""
    risk_input = RiskInput(**base_input_dict)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.ALLOW
    assert "normal operating parameters" in directive.reason

def test_allow_state_at_new_equity_high(governor, base_input_dict):
    """Test that the reason for ALLOW mentions new equity high when applicable."""
    kwargs = base_input_dict.copy()
    kwargs['is_new_equity_high'] = True
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.ALLOW
    assert "System at new equity high" in directive.reason

def test_priority_of_rules(governor, base_input_dict):
    """
    Test that a higher priority rule (e.g., BLOCK) overrides a lower one (e.g., RESTRICT).
    Here, data integrity failure should trump low regime confidence.
    """
    kwargs = base_input_dict.copy()
    kwargs['data_integrity_score'] = 0.7
    kwargs['regime_confidence'] = 0.5
    risk_input = RiskInput(**kwargs)
    directive = governor.assess_risk(risk_input)
    assert directive.permission_state == PermissionState.BLOCK
    assert "data integrity failure" in directive.reason # Confirms the first rule was hit
