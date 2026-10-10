import numpy as np
import pandas as pd
import pytest

from scripts.download_data import TICKERS, to_long_format, validate

COLUMNS = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]


def make_raw():
    """Mimic yfinance's multi-ticker output: columns are (Price, Ticker)."""
    index = pd.DatetimeIndex(["2024-01-02", "2024-01-03"], name="Date")
    columns = pd.MultiIndex.from_product(
        [["Close", "High", "Low", "Open", "Volume"], ["AAA", "BBB"]], names=["Price", "Ticker"]
    )
    return pd.DataFrame(np.arange(1, 21, dtype=float).reshape(2, 10) + 0.123456, index=index, columns=columns)


def test_ticker_list():
    assert len(TICKERS) == 24 and len(set(TICKERS)) == 24
    assert TICKERS[0] == "SPY" and TICKERS[-1] == "GLD"


def test_to_long_format_shape_and_order():
    long = to_long_format(make_raw())
    assert list(long.columns) == COLUMNS
    assert long["Ticker"].tolist() == ["AAA", "AAA", "BBB", "BBB"]
    assert long["Volume"].dtype == "int64"
    assert long["Close"].iloc[0] == pytest.approx(1.1235)


def test_to_long_format_drops_days_without_prices():
    raw = make_raw()
    raw.loc["2024-01-02", ("Close", "BBB")] = np.nan
    long = to_long_format(raw)
    assert len(long[long["Ticker"] == "BBB"]) == 1


def test_validate_passes_clean_data():
    validate(to_long_format(make_raw()), ["AAA", "BBB"])


def test_validate_flags_missing_ticker():
    with pytest.raises(ValueError, match="CCC"):
        validate(to_long_format(make_raw()), ["AAA", "BBB", "CCC"])


def test_validate_flags_nan_prices():
    long = to_long_format(make_raw())
    long.loc[0, "Open"] = np.nan
    with pytest.raises(ValueError, match="missing prices"):
        validate(long, ["AAA", "BBB"])


def test_validate_flags_duplicates():
    long = to_long_format(make_raw())
    long = pd.concat([long, long.iloc[[0]]])
    with pytest.raises(ValueError, match="duplicate"):
        validate(long, ["AAA", "BBB"])
