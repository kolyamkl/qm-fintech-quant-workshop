"""Charts for backtest results (matplotlib).

Each function returns a matplotlib Figure. In a notebook, make it the last
line of a cell to display it; in Streamlit, pass it to st.pyplot().
"""

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from .metrics import drawdown_series

# Same colours in every chart, so "Strategy" and "Buy & hold" are easy to tell apart.
STRATEGY_COLOR = "tab:blue"
BENCHMARK_COLOR = "tab:orange"


def _figure_and_axes(ax, figsize=(10, 4)):
    if ax is None:
        fig = Figure(figsize=figsize)
        ax = fig.subplots()
    return ax.figure, ax


def plot_equity(result, ax=None) -> Figure:
    """Portfolio value over time: strategy vs buy-and-hold."""
    fig, ax = _figure_and_axes(ax)
    ax.plot(result.equity.index, result.equity, label="Strategy", color=STRATEGY_COLOR)
    ax.plot(result.benchmark_equity.index, result.benchmark_equity, label="Buy & hold", color=BENCHMARK_COLOR, alpha=0.7)
    ax.set_title("Portfolio value")
    ax.set_ylabel("$")
    ax.legend()
    ax.grid(alpha=0.3)
    return fig


def plot_drawdown(result, ax=None) -> Figure:
    """How far below its previous peak each portfolio was, in %."""
    fig, ax = _figure_and_axes(ax)
    strategy = drawdown_series(result.equity) * 100
    benchmark = drawdown_series(result.benchmark_equity) * 100
    ax.fill_between(strategy.index, strategy, 0, alpha=0.4, label="Strategy", color=STRATEGY_COLOR)
    ax.plot(benchmark.index, benchmark, label="Buy & hold", color=BENCHMARK_COLOR, alpha=0.7)
    ax.set_title("Drawdown (% below previous peak)")
    ax.set_ylabel("%")
    ax.legend()
    ax.grid(alpha=0.3)
    return fig


def plot_result(result) -> Figure:
    """Portfolio value on top, drawdown underneath."""
    fig = Figure(figsize=(10, 7))
    top, bottom = fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    plot_equity(result, ax=top)
    plot_drawdown(result, ax=bottom)
    fig.tight_layout()
    return fig


def plot_signals(prices, result, overlays=None, ax=None) -> Figure:
    """Price with optional indicator lines and markers where trades opened (▲) and closed (▼).

    A trade still open when the data ends gets no ▼ — it was never actually closed.

    overlays: dict of label -> Series, e.g. {"50-day MA": close.rolling(50).mean()}
    """
    fig, ax = _figure_and_axes(ax, figsize=(10, 5))
    ax.plot(prices.index, prices["Close"], label="Close", color="black", linewidth=1)
    for label, line in (overlays or {}).items():
        ax.plot(line.index, line, label=label, linewidth=1.2)

    trades = result.trades
    closed = trades[~trades["open"].astype(bool)]
    ax.scatter(trades["entry_date"], trades["entry_price"], marker="^", s=70, color="tab:green", label="Enter", zorder=3)
    ax.scatter(closed["exit_date"], closed["exit_price"], marker="v", s=70, color="tab:red", label="Exit", zorder=3)
    ax.set_title("Price and trades")
    ax.legend()
    ax.grid(alpha=0.3)
    return fig


def plot_heatmap(table, title, highlight=None, vmin=None, vmax=None, ax=None) -> Figure:
    """A coloured grid of one number (e.g. Sharpe) for every pair of settings.

    table: DataFrame whose rows and columns are the two settings (e.g. fast x slow MA).
           NaN cells (e.g. impossible pairs) stay blank.
    highlight: optional (row, column) to outline, e.g. the best settings.
    vmin / vmax: fix the colour scale, so two heatmaps can be compared fairly.
    """
    fig, ax = _figure_and_axes(ax, figsize=(6, 4.5))
    image = ax.imshow(table.to_numpy(dtype=float), cmap="RdYlGn", vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(table.columns)), labels=table.columns)
    ax.set_yticks(range(len(table.index)), labels=table.index)
    ax.set_xlabel(table.columns.name or "")
    ax.set_ylabel(table.index.name or "")
    for i, row in enumerate(table.index):
        for j, column in enumerate(table.columns):
            value = table.loc[row, column]
            if pd.notna(value):
                ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8)
    if highlight is not None:
        i, j = table.index.get_loc(highlight[0]), table.columns.get_loc(highlight[1])
        ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor="black", linewidth=2.5))
    fig.colorbar(image, ax=ax)
    ax.set_title(title)
    return fig
