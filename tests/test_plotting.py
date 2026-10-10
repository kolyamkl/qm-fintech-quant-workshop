import pandas as pd
from matplotlib.figure import Figure

from backtester import run_backtest
from backtester.plotting import plot_drawdown, plot_equity, plot_result, plot_signals


def make_result(make_prices, positions):
    prices = make_prices([100, 101, 103, 102, 104])
    return prices, run_backtest(prices, pd.Series(positions, index=prices.index))


def test_plot_result_has_equity_and_drawdown(make_prices):
    _, result = make_result(make_prices, [1, 1, 1, 1, 1])
    fig = result.plot()
    assert isinstance(fig, Figure)
    assert len(fig.axes) == 2


def test_single_plots_return_figures(make_prices):
    _, result = make_result(make_prices, [1, 1, 1, 1, 1])
    assert isinstance(plot_equity(result), Figure)
    assert isinstance(plot_drawdown(result), Figure)
    assert len(plot_result(result).axes[0].get_lines()) == 2  # strategy + buy & hold


def test_plot_signals_draws_overlays_and_trade_markers(make_prices):
    prices, result = make_result(make_prices, [0, 1, 1, 0, 0])
    overlay = prices["Close"].rolling(2).mean()
    fig = plot_signals(prices, result, overlays={"2-day MA": overlay})
    ax = fig.axes[0]
    assert len(ax.get_lines()) == 2  # close + overlay
    assert len(ax.collections) == 2  # entry markers + exit markers
