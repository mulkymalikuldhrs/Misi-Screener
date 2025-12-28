"""
Unit tests for the Regime Classification Engine.
"""
import pytest
from core.regime.engine import RegimeEngine, RegimeInput, Regime

@pytest.fixture
def engine():
    """Provides a RegimeEngine instance."""
    return RegimeEngine()

def test_rule_1_stress_breakdown_regime(engine):
    """Tests that extreme volatility and low structure stability correctly classify as STRESS_BREAKDOWN."""
    inputs = RegimeInput(
        atr_percentile=0.96,
        structure_stability=0.1,
        participation_score=80
    )
    output = engine.classify_regime(inputs)
    assert output.regime == Regime.STRESS_BREAKDOWN
    assert output.confidence > 0.8
    assert "trend_following" in output.incompatible_actions

def test_rule_2_compression_regime(engine):
    """Tests that low volatility and low participation correctly classify as COMPRESSION."""
    inputs = RegimeInput(
        atr_percentile=0.15,
        structure_stability=0.5, # Structure should not matter
        participation_score=25
    )
    output = engine.classify_regime(inputs)
    assert output.regime == Regime.COMPRESSION
    assert output.confidence > 0.6
    assert "breakout" in output.incompatible_actions

def test_rule_3_expansion_regime(engine):
    """Tests that high volatility, stability, and participation classify as EXPANSION."""
    inputs = RegimeInput(
        atr_percentile=0.8,
        structure_stability=0.7,
        participation_score=75
    )
    output = engine.classify_regime(inputs)
    assert output.regime == Regime.EXPANSION
    assert output.confidence > 0.7
    assert "mean_reversion" in output.incompatible_actions

def test_rule_4_mean_reversion_regime(engine):
    """Tests that medium-high volatility and low structure stability classify as MEAN_REVERSION."""
    inputs = RegimeInput(
        atr_percentile=0.7,
        structure_stability=0.3,
        participation_score=60 # Participation is moderate
    )
    output = engine.classify_regime(inputs)
    assert output.regime == Regime.MEAN_REVERSION
    assert output.confidence > 0.6
    assert "trend_following" in output.incompatible_actions

def test_default_transition_regime(engine):
    """Tests that inputs not matching any specific rule default to TRANSITION."""
    inputs = RegimeInput(
        atr_percentile=0.5,
        structure_stability=0.5,
        participation_score=50
    )
    output = engine.classify_regime(inputs)
    assert output.regime == Regime.TRANSITION
    assert output.confidence == 0.5
    assert len(output.incompatible_actions) == 0

def test_determinism(engine):
    """Tests that the same input always produces the same output."""
    inputs = RegimeInput(
        atr_percentile=0.8,
        structure_stability=0.7,
        participation_score=75
    )
    output1 = engine.classify_regime(inputs)
    output2 = engine.classify_regime(inputs)
    assert output1 == output2
