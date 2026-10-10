import datetime as dt

import pandas as pd
import pytest

import backtester.data as data

CSV = """Date,Ticker,Open,High,Low,Close,Volume
2024-01-02,AAA,1,2,0.5,1.5,100
2024-01-03,AAA,1.5,2.5,1,2,200
2024-01-04,AAA,2,3,1.5,2.5,300
2024-01-02,BBB,10,11,9,10.5,1000
2024-01-03,BBB,10.5,12,10,11,2000
2024-01-04,BBB,11,13,10.5,12,3000
"""


@pytest.fixture
def tiny_data(tmp_path, monkeypatch):
    path = tmp_path / "prices.csv"
    path.write_text(CSV)
    monkeypatch.setattr(data, "DATA_PATH", path)
    data._load_all.cache_clear()
    yield
    data._load_all.cache_clear()


def test_load_prices_shape(tiny_data):
    prices = data.load_prices("AAA")
    assert list(prices.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert prices.index.name == "Date"
    assert isinstance(prices.index, pd.DatetimeIndex)
    assert prices["Close"].tolist() == [1.5, 2, 2.5]


def test_ticker_is_case_and_space_insensitive(tiny_data):
    assert data.load_prices(" aaa ")["Close"].iloc[-1] == 2.5


def test_unknown_ticker_lists_available(tiny_data):
    with pytest.raises(ValueError, match="AAA, BBB"):
        data.load_prices("ZZZ")


def test_start_end_accept_strings_and_dates(tiny_data):
    assert len(data.load_prices("AAA", start="2024-01-03")) == 2
    assert len(data.load_prices("AAA", end=dt.date(2024, 1, 3))) == 2
    assert len(data.load_prices("AAA", start=dt.date(2024, 1, 3), end="2024-01-03")) == 1
    assert len(data.load_prices("AAA", start="2025-01-01")) == 0


def test_load_closes_is_wide(tiny_data):
    closes = data.load_closes(["AAA", "BBB"])
    assert list(closes.columns) == ["AAA", "BBB"]
    assert closes.loc["2024-01-04", "BBB"] == 12
    assert list(data.load_closes("AAA").columns) == ["AAA"]


def test_available_tickers_sorted(tiny_data):
    assert data.available_tickers() == ["AAA", "BBB"]


@pytest.mark.skipif(not data.DATA_PATH.exists(), reason="data/prices.csv not generated yet")
def test_real_dataset_is_clean():
    data._load_all.cache_clear()
    df = data._load_all()
    assert list(df.columns) == ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    assert df[["Open", "High", "Low", "Close"]].notna().all().all()
    assert not df.duplicated(["Date", "Ticker"]).any()
    assert df["Ticker"].nunique() == 24
    assert df["Date"].min() < pd.Timestamp("2016-01-10")
