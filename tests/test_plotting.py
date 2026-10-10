import pandas as pd
from matplotlib.colors import to_hex
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


def test_strategy_and_benchmark_keep_their_colours_across_charts(make_prices):
    _, result = make_result(make_prices, [0, 1, 1, 0, 0])
    equity_ax, drawdown_ax = plot_result(result).axes
    strategy_line, benchmark_line = equity_ax.get_lines()
    strategy_fill = drawdown_ax.collections[0]
    (drawdown_benchmark_line,) = drawdown_ax.get_lines()
    assert drawdown_benchmark_line.get_color() == benchmark_line.get_color()
    assert to_hex(strategy_fill.get_facecolor()[0]) == to_hex(strategy_line.get_color())
    assert strategy_line.get_color() != benchmark_line.get_color()


def test_trade_still_open_at_the_end_gets_no_exit_marker(make_prices):
    prices, result = make_result(make_prices, [0, 1, 1, 1, 1])
    entries, exits = plot_signals(prices, result).axes[0].collections
    assert len(entries.get_offsets()) == 1
    assert len(exits.get_offsets()) == 0
