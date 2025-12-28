"""
Unit tests for the Market Structure Engine.
"""
import pytest
import pandas as pd
from core.structure.engine import MarketStructureEngine, SwingType

@pytest.fixture
def sample_ohlc_data():
    """
    Provides a sample OHLC DataFrame for testing.
    This data includes a clear swing high and a clear swing low.
    """
    data = {
        'timestamp': pd.to_datetime([
            '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
            '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10'
        ]),
        'open':  [100, 102, 105, 103, 106, 110, 108, 105, 103, 101],
        'high':  [103, 106, 108, 105, 109, 112, 110, 107, 105, 104],
        'low':   [99,  101, 104, 102, 105, 109, 107, 104, 102, 100],
        'close': [102, 105, 107, 104, 108, 111, 109, 106, 104, 102]
    }
    return pd.DataFrame(data)

def test_deterministic_swing_detection(sample_ohlc_data):
    """
    Tests that the engine produces the same output for the same input.
    """
    engine = MarketStructureEngine()

    # Run the analysis twice
    output1 = engine.analyze_structure(sample_ohlc_data, lookback_period=2)
    output2 = engine.analyze_structure(sample_ohlc_data, lookback_period=2)

    # Assert that the outputs are identical
    assert output1 == output2

def test_swing_high_detection(sample_ohlc_data):
    """
    Tests that a clear swing high is correctly identified.
    The swing high is on 2023-01-06 with a high of 112.
    """
    engine = MarketStructureEngine()
    output = engine.analyze_structure(sample_ohlc_data, lookback_period=2)

    swing_highs = [p for p in output.swing_points if p.swing_type == SwingType.HIGH]

    assert len(swing_highs) == 1
    assert swing_highs[0].timestamp == pd.to_datetime('2023-01-06')
    assert swing_highs[0].price == 112

def test_swing_low_detection(sample_ohlc_data):
    """
    Tests that a clear swing low is correctly identified.
    The swing low is on 2023-01-01 with a low of 99, but it's at the start.
    A clearer one for the test is on 2023-01-04 with a low of 102.
    Let's adjust data for a clearer swing low.
    """

    data = {
        'timestamp': pd.to_datetime([
            '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
            '2023-01-06', '2023-01-07'
        ]),
        'open':  [110, 108, 105, 103, 106, 108, 110],
        'high':  [112, 110, 107, 105, 109, 111, 112],
        'low':   [108, 106, 103, 100, 102, 105, 109],
        'close': [109, 107, 104, 102, 105, 107, 111]
    }
    df = pd.DataFrame(data)
    engine = MarketStructureEngine()
    output = engine.analyze_structure(df, lookback_period=2)

    swing_lows = [p for p in output.swing_points if p.swing_type == SwingType.LOW]

    assert len(swing_lows) == 1
    assert swing_lows[0].timestamp == pd.to_datetime('2023-01-04')
    assert swing_lows[0].price == 100

def test_no_swing_points_in_strong_trend():
    """
    Tests that no swing points are found in a strong, monotonic trend.
    """
    data = {
        'timestamp': pd.to_datetime([
            '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
            '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10'
        ]),
        'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'low':  [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    }
    df = pd.DataFrame(data)
    engine = MarketStructureEngine()
    output = engine.analyze_structure(df, lookback_period=2)

    assert len(output.swing_points) == 0
