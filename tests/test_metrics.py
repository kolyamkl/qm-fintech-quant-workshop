import math

import numpy as np
import pandas as pd
import pytest

from backtester.metrics import (
    annual_volatility,
    cagr,
    compute_metrics,
    drawdown_series,
    format_metrics,
    max_drawdown,
    sharpe_ratio,
    total_return,
    win_rate,
)


def test_total_return():
    assert total_return(pd.Series([100.0, 110.0, 99.0])) == pytest.approx(-0.01)


def test_cagr_one_year_of_ten_percent():
    equity = pd.Series(np.linspace(100, 110, 253))  # 252 daily steps = 1 year
    assert cagr(equity) == pytest.approx(0.10)


def test_cagr_single_point_is_nan():
    assert math.isnan(cagr(pd.Series([100.0])))


def test_annual_volatility():
    assert annual_volatility(pd.Series([0.01, -0.01])) == pytest.approx(0.224499, rel=1e-5)


def test_sharpe_ratio():
    assert sharpe_ratio(pd.Series([0.01, -0.01, 0.02, 0.0])) == pytest.approx(6.14817, rel=1e-4)


def test_sharpe_ratio_zero_volatility_is_nan():
    assert math.isnan(sharpe_ratio(pd.Series([0.0, 0.0, 0.0])))
    assert math.isnan(sharpe_ratio(pd.Series([0.01, 0.01, 0.01])))


def test_drawdown_and_max_drawdown():
    equity = pd.Series([100.0, 110.0, 99.0, 120.0])
    assert drawdown_series(equity).tolist() == pytest.approx([0.0, 0.0, -0.1, 0.0])
    assert max_drawdown(equity) == pytest.approx(-0.1)


def test_win_rate_counts_only_positive_returns():
    trades = pd.DataFrame({"return": [0.1, -0.05, 0.02, 0.0]})
    assert win_rate(trades) == pytest.approx(0.5)


def test_win_rate_without_trades_is_nan():
    assert math.isnan(win_rate(pd.DataFrame({"return": []})))
    assert math.isnan(win_rate(None))


def test_compute_metrics_keys_and_trade_count():
    equity = pd.Series([100.0, 101.0, 102.0])
    returns = pd.Series([0.01, 0.0099])
    trades = pd.DataFrame({"return": [0.02]})
    metrics = compute_metrics(equity, returns, trades)
    assert list(metrics) == [
        "Total return",
        "Annual return (CAGR)",
        "Annual volatility",
        "Sharpe ratio",
        "Max drawdown",
        "Number of trades",
        "Win rate",
    ]
    assert metrics["Number of trades"] == 1
    assert math.isnan(compute_metrics(equity, returns)["Number of trades"])


def test_format_metrics():
    formatted = format_metrics(
        {"Total return": 0.1234, "Sharpe ratio": 1.234, "Number of trades": 3, "Win rate": float("nan")}
    )
    assert formatted == {"Total return": "12.3%", "Sharpe ratio": "1.23", "Number of trades": "3", "Win rate": "—"}
