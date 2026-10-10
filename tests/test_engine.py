import math

import pandas as pd
import pytest

from backtester.engine import run_backtest


def series(values, prices):
    return pd.Series(values, index=prices.index, dtype=float)


def test_always_long_without_costs_equals_buy_and_hold(make_prices):
    prices = make_prices([100, 101, 99, 105, 110])
    result = run_backtest(prices, series([1] * 5, prices), cost_bps=0)
    assert result.equity.tolist() == pytest.approx(result.benchmark_equity.tolist())
    assert result.equity.iloc[-1] == pytest.approx(11_000)


def test_always_flat_keeps_cash_and_metrics_are_nan_safe(make_prices):
    prices = make_prices([100, 101, 99, 105, 110])
    result = run_backtest(prices, series([0] * 5, prices))
    assert result.equity.tolist() == pytest.approx([10_000] * 5)
    assert math.isnan(result.metrics["Sharpe ratio"])
    assert math.isnan(result.metrics["Win rate"])
    assert result.metrics["Number of trades"] == 0
    assert len(result.trades) == 0


def test_signal_cannot_earn_the_return_of_the_day_it_was_made(make_prices):
    prices = make_prices([100, 100, 200, 200])
    # Decided at day 2's close (the jump day): too late to profit from the jump.
    late = run_backtest(prices, series([0, 0, 1, 1], prices), cost_bps=0)
    assert late.equity.iloc[-1] == pytest.approx(10_000)
    # Decided at day 1's close: held during day 2, so it earns the jump.
    early = run_backtest(prices, series([0, 1, 1, 1], prices), cost_bps=0)
    assert early.equity.iloc[-1] == pytest.approx(20_000)


def test_entry_cost_is_charged_once(make_prices):
    prices = make_prices([100] * 5)
    result = run_backtest(prices, series([1] * 5, prices), cost_bps=10)
    assert result.equity.iloc[-1] == pytest.approx(10_000 * (1 - 0.001))


def test_flipping_long_to_short_costs_double(make_prices):
    prices = make_prices([100] * 5)
    result = run_backtest(prices, series([1, -1, -1, -1, -1], prices), cost_bps=10)
    assert result.equity.iloc[-1] == pytest.approx(10_000 * (1 - 0.001) * (1 - 0.002))


def test_short_position_profits_when_price_falls(make_prices):
    prices = make_prices([100, 90])
    result = run_backtest(prices, series([-1, -1], prices), cost_bps=0)
    assert result.equity.iloc[-1] == pytest.approx(11_000)


def test_nan_positions_are_treated_as_flat(make_prices):
    prices = make_prices([100, 101, 102, 103, 104])
    result = run_backtest(prices, series([float("nan"), float("nan"), 1, 1, 1], prices))
    assert result.positions.tolist() == [0, 0, 0, 1, 1]


def test_boolean_positions_are_accepted(make_prices):
    prices = make_prices([100, 101, 102, 103])
    as_bool = pd.Series([False, True, True, True], index=prices.index)
    as_int = series([0, 1, 1, 1], prices)
    assert run_backtest(prices, as_bool).equity.tolist() == pytest.approx(run_backtest(prices, as_int).equity.tolist())


def test_positions_are_aligned_to_price_dates(make_prices):
    prices = make_prices([100, 101, 102, 103, 104])
    positions = series([1] * 5, prices)  # computed on the full history
    result = run_backtest(prices.iloc[2:], positions)  # backtest only the last 3 days
    assert len(result.equity) == 3


def test_invalid_position_values_raise(make_prices):
    prices = make_prices([100, 101, 102])
    with pytest.raises(ValueError, match="-1, 0 or 1"):
        run_backtest(prices, series([0, 2, 1], prices))


def test_too_few_rows_raises(make_prices):
    prices = make_prices([100])
    with pytest.raises(ValueError, match="at least 2"):
        run_backtest(prices, series([1], prices))


def test_trades_are_listed_with_returns(make_prices):
    prices = make_prices([10, 10, 12, 15, 15, 12, 12])
    result = run_backtest(prices, series([0, 1, 1, 0, -1, -1, 0], prices))
    trades = result.trades
    assert trades["direction"].tolist() == ["long", "short"]
    assert trades["entry_price"].tolist() == [10, 15]
    assert trades["exit_price"].tolist() == [15, 12]
    assert trades["return"].tolist() == pytest.approx([0.5, 0.2])
    assert trades["entry_date"].tolist() == [prices.index[1], prices.index[4]]


def test_open_trade_is_closed_on_last_day(make_prices):
    prices = make_prices([10, 10, 12])
    result = run_backtest(prices, series([0, 1, 1], prices))
    assert len(result.trades) == 1
    assert result.trades["exit_date"].iloc[0] == prices.index[-1]
    assert result.trades["return"].iloc[0] == pytest.approx(0.2)


def test_summary_compares_strategy_and_benchmark(make_prices):
    prices = make_prices([100, 101, 102, 103])
    summary = run_backtest(prices, series([1] * 4, prices)).summary()
    assert list(summary.columns) == ["Strategy", "Buy & hold"]
    assert "Sharpe ratio" in summary.index
    assert summary.loc["Number of trades", "Buy & hold"] == "—"
