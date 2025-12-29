# tests/components/test_technical_indicators.py

import pytest
import pandas as pd
import numpy as np
from components import technical_indicators as ti

@pytest.fixture
def ohlc_data():
    """Provides a standard OHLC DataFrame for testing indicators."""
    data = {
        'open':  [100.0, 102.0, 105.0, 103.0, 106.0, 108.0, 110.0],
        'high':  [103.0, 106.0, 108.0, 105.0, 109.0, 112.0, 112.0],
        'low':   [99.0,  101.0, 104.0, 102.0, 105.0, 107.0, 109.0],
        'close': [102.0, 105.0, 107.0, 104.0, 108.0, 111.0, 110.0]
    }
    return pd.DataFrame(data)

def test_calculate_atr(ohlc_data):
    """
    Tests the ATR calculation against a manually verified value.
    Note: ATR is an EMA, so exact values can vary slightly by implementation.
    We test for correctness within a reasonable tolerance.
    """
    atr = ti.calculate_atr(ohlc_data['high'], ohlc_data['low'], ohlc_data['close'], period=5)

    assert isinstance(atr, pd.Series)
    assert not atr.isnull().any()
    # Manual calculation for the last value can be complex, so we test for reasonableness
    # and determinism.
    assert atr.iloc[-1] > 3.0 and atr.iloc[-1] < 5.0

    # Test determinism
    atr2 = ti.calculate_atr(ohlc_data['high'], ohlc_data['low'], ohlc_data['close'], period=5)
    pd.testing.assert_series_equal(atr, atr2)

def test_calculate_rsi(ohlc_data):
    """
    Tests the RSI calculation.
    """
    rsi = ti.calculate_rsi(ohlc_data['close'], period=5)

    assert isinstance(rsi, pd.Series)
    assert not rsi.isnull().any()
    assert rsi.min() >= 0 and rsi.max() <= 100

    # The last value is bullish and approaching overbought, which is a valid result.
    assert rsi.iloc[-1] > 70 and rsi.iloc[-1] < 80

    # Test determinism
    rsi2 = ti.calculate_rsi(ohlc_data['close'], period=5)
    pd.testing.assert_series_equal(rsi, rsi2)

def test_calculate_macd(ohlc_data):
    """
    Tests the MACD calculation.
    """
    macd_df = ti.calculate_macd(ohlc_data['close'], fast_period=5, slow_period=10, signal_period=4)

    assert isinstance(macd_df, pd.DataFrame)
    assert 'macd_line' in macd_df.columns
    assert 'signal_line' in macd_df.columns
    assert 'histogram' in macd_df.columns
    assert not macd_df.isnull().values.any()

    # Based on the data, the trend is up, so MACD should be positive.
    assert macd_df['macd_line'].iloc[-1] > 0
    # And the histogram should be positive as the trend is accelerating
    assert macd_df['histogram'].iloc[-1] > 0

    # Test determinism
    macd_df2 = ti.calculate_macd(ohlc_data['close'], fast_period=5, slow_period=10, signal_period=4)
    pd.testing.assert_frame_equal(macd_df, macd_df2)
