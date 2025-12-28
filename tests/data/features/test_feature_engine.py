"""
Unit tests for the Feature Engine.
"""
import pytest
import pandas as pd
from data.features.engine import FeatureEngine

@pytest.fixture
def feature_engine():
    """Provides a FeatureEngine instance."""
    return FeatureEngine()

@pytest.fixture
def ohlc_data():
    """Provides a sample OHLC DataFrame for testing."""
    data = {
        'open':  [100, 102, 105, 103, 106],
        'high':  [103, 106, 108, 105, 109],
        'low':   [99,  101, 104, 102, 105],
        'close': [102, 105, 107, 104, 108]
    }
    return pd.DataFrame(data)

def test_heikin_ashi_calculation(feature_engine, ohlc_data):
    """
    Tests the Heikin-Ashi calculation against a known result.
    The expected values are calculated manually or from a trusted source.
    """
    ha_df = feature_engine.calculate_heikin_ashi(ohlc_data)

    # --- Expected Values ---
    # Bar 0:
    # ha_close = (100+103+99+102)/4 = 101.0
    # ha_open = (100+102)/2 = 101.0
    # ha_high = max(103, 101.0, 101.0) = 103.0
    # ha_low = min(99, 101.0, 101.0) = 99.0
    #
    # Bar 1:
    # ha_close = (102+106+101+105)/4 = 103.5
    # ha_open = (101.0 + 101.0)/2 = 101.0
    # ha_high = max(106, 101.0, 103.5) = 106.0
    # ha_low = min(101, 101.0, 103.5) = 101.0

    assert ha_df['ha_close'].iloc[0] == pytest.approx(101.0)
    assert ha_df['ha_open'].iloc[0] == pytest.approx(101.0)
    assert ha_df['ha_high'].iloc[0] == pytest.approx(103.0)
    assert ha_df['ha_low'].iloc[0] == pytest.approx(99.0)

    assert ha_df['ha_close'].iloc[1] == pytest.approx(103.5)
    assert ha_df['ha_open'].iloc[1] == pytest.approx(101.0)
    assert ha_df['ha_high'].iloc[1] == pytest.approx(106.0)
    assert ha_df['ha_low'].iloc[1] == pytest.approx(101.0)

    # Check for determinism
    ha_df2 = feature_engine.calculate_heikin_ashi(ohlc_data)
    pd.testing.assert_frame_equal(ha_df, ha_df2)

def test_output_shape(feature_engine, ohlc_data):
    """
    Tests that the output DataFrame has the correct shape and columns.
    """
    ha_df = feature_engine.calculate_heikin_ashi(ohlc_data)
    assert ha_df.shape[0] == ohlc_data.shape[0]
    assert 'ha_open' in ha_df.columns
    assert 'ha_high' in ha_df.columns
    assert 'ha_low' in ha_df.columns
    assert 'ha_close' in ha_df.columns
