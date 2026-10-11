"""Interactive backtester for the QM FinTech Society quant workshop.

Run it locally from the repo folder:
    streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

# Make `backtester` and `strategies` importable however the app is launched.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from backtester import available_tickers, load_prices, run_backtest
from backtester.metrics import format_metrics
from backtester.plotting import plot_heatmap, plot_result, plot_signals
from strategies import ma_crossover, rsi_mean_reversion

METRIC_HELP = {
    "Total return": "How much the $10,000 starting portfolio grew (or shrank) over the whole period, after trading costs.",
    "Annual return (CAGR)": "The steady yearly growth rate that would give the same total return. "
    "It makes periods of different lengths comparable.",
    "Sharpe ratio": "Return per unit of risk: the average daily return divided by how much daily returns swing, "
    "scaled to a year (risk-free rate taken as 0). Higher is better.",
    "Max drawdown": "The worst fall from a previous high: the most painful loss you would have had to sit through.",
}

# Overfitting lab: the same train/test split as notebook 01.
TRAIN_END, TEST_START = "2021-12-31", "2022-01-01"
LAB_FASTS = [10, 20, 30, 40, 50, 75, 100]
LAB_SLOWS = [50, 100, 150, 200, 250, 300]


@st.cache_data
def ma_sharpe_grids(ticker: str, cost_bps: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Sharpe of every fast/slow MA crossover on the training period and on the test period."""
    prices = load_prices(ticker)
    train = pd.DataFrame(
        index=pd.Index(LAB_FASTS, name="Fast MA (days)"),
        columns=pd.Index(LAB_SLOWS, name="Slow MA (days)"),
        dtype=float,
    )
    test = train.copy()
    for fast in LAB_FASTS:
        for slow in LAB_SLOWS:
            if fast >= slow:
                continue  # not a valid crossover: stays blank
            positions = ma_crossover(prices, fast=fast, slow=slow)
            for table, window in ((train, slice(None, TRAIN_END)), (test, slice(TEST_START, None))):
                result = run_backtest(prices.loc[window], positions.loc[window], cost_bps=cost_bps)
                table.loc[fast, slow] = result.metrics["Sharpe ratio"]
    return train, test


def overfitting_lab(ticker: str, cost_bps: float) -> None:
    st.markdown(
        f"Try enough settings and one of them will look brilliant on past data, **by luck**. "
        f"Here every fast/slow pair of the moving-average crossover is backtested on **{ticker}** twice: "
        f"on **2016–2021** (*training*, where you would pick your settings) and on **2022 onwards** "
        f"(*test*, data your choice never saw). The outlined cell is the training winner."
    )
    train, test = ma_sharpe_grids(ticker, cost_bps)
    best = train.stack().dropna().idxmax()
    test_ranks = test.stack().dropna().rank(ascending=False)
    low = min(train.min().min(), test.min().min())
    high = max(train.max().max(), test.max().max())

    left, right = st.columns(2)
    left.pyplot(plot_heatmap(train, "Training: Sharpe 2016–2021", highlight=best, vmin=low, vmax=high))
    right.pyplot(plot_heatmap(test, "Test: Sharpe 2022 onwards", highlight=best, vmin=low, vmax=high))

    st.info(
        f"The best settings on 2016–2021 were **fast {best[0]} / slow {best[1]}**, with a Sharpe of "
        f"**{train.loc[best]:.2f}**. On 2022 onwards the same settings scored **{test.loc[best]:.2f}**, "
        f"ranking **{test_ranks.get(best, float('nan')):.0f} of {len(test_ranks)}**."
    )
    st.markdown(
        "If the training winner slides down the ranking on new data, part of its result was luck: that's "
        "**overfitting**. Real research keeps a test period untouched until the very end, and prefers settings "
        "that are good across a whole *neighbourhood* of the grid, not one lucky cell."
    )
    st.caption(
        "Uses the ticker and trading cost from the sidebar; ignores the strategy choice and date range. "
        "Green = higher Sharpe, red = lower. Blank cells: the fast average must be shorter than the slow one."
    )


st.set_page_config(page_title="Algo Trading Backtester", page_icon="📈", layout="wide")
st.title("📈 Algo trading backtester")
st.caption(
    "QM FinTech Society quant workshop · Educational use only — not financial advice. "
    "Price data from Yahoo Finance; no ownership is claimed."
)

with st.expander("📖 New here? How to use this app"):
    st.markdown(
        """
1. **Pick a ticker and a strategy** in the sidebar (on a phone, open it with the arrow at the top left).
2. **Move the sliders.** The page updates with the new backtest.
3. **Compare with buy & hold.** The big numbers are the strategy; the grey labels underneath are what simply
   buying and holding the same ticker did over the same dates. Hover the **?** next to a name for what it means.
4. **Open the 🎯 Overfitting lab tab** to see why the "best" settings on past data often disappoint later.
"""
    )

tickers = available_tickers()

with st.sidebar:
    st.header("Settings")
    ticker = st.selectbox("Ticker", tickers, index=tickers.index("SPY"))
    strategy = st.radio("Strategy", ["MA crossover", "RSI mean reversion"])
    if strategy == "MA crossover":
        fast = st.slider("Fast moving average (days)", 5, 100, 50)
        slow = st.slider("Slow moving average (days)", 20, 300, 200)
    else:
        period = st.slider("RSI period (days)", 2, 30, 14)
        lower, upper = st.slider("Buy below / sell above (RSI)", 5, 95, (30, 70))
    cost_bps = st.number_input(
        "Trading cost per trade (bps, 1 bp = 0.01%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0
    )
    full_history = load_prices(ticker)
    first_day, last_day = full_history.index[0].date(), full_history.index[-1].date()
    dates = st.date_input("Date range", value=(first_day, last_day), min_value=first_day, max_value=last_day)

backtest_tab, lab_tab = st.tabs(["📊 Backtest", "🎯 Overfitting lab"])

# The lab is drawn first: the backtest tab may stop early (st.stop) on invalid settings.
with lab_tab:
    overfitting_lab(ticker, cost_bps)

with backtest_tab:
    if len(dates) != 2:
        st.info("Pick an end date to finish selecting the date range.")
        st.stop()

    # Indicators are computed on the full history (they only look backwards),
    # so a short date range still gets properly warmed-up moving averages.
    if strategy == "MA crossover":
        if fast >= slow:
            st.warning("The fast moving average must be shorter than the slow one — adjust the sliders.")
            st.stop()
        positions = ma_crossover(full_history, fast=fast, slow=slow)
        close = full_history["Close"]
        overlays = {f"{fast}-day MA": close.rolling(fast).mean(), f"{slow}-day MA": close.rolling(slow).mean()}
        rule = (
            f"Blue and orange: the {fast}- and {slow}-day moving averages. "
            f"The strategy holds {ticker} while the fast (blue) average is above the slow (orange) one."
        )
    else:
        if lower >= upper:
            st.warning("The buy level must be below the sell level — adjust the slider.")
            st.stop()
        positions = rsi_mean_reversion(full_history, period=period, lower=lower, upper=upper)
        overlays = {}
        rule = (
            f"The strategy buys when the {period}-day RSI falls below {lower} (the price has dropped a lot) "
            f"and sells when it rises above {upper}."
        )

    window = slice(pd.Timestamp(dates[0]), pd.Timestamp(dates[1]))
    prices = full_history.loc[window]
    if len(prices) < 2:
        st.warning("Pick a date range of at least two trading days.")
        st.stop()

    result = run_backtest(prices, positions.loc[window], cost_bps=cost_bps)

    strategy_metrics = format_metrics(result.metrics)
    benchmark_metrics = format_metrics(result.benchmark_metrics)
    for column, name in zip(st.columns(4), METRIC_HELP):
        column.metric(
            name,
            strategy_metrics[name],
            f"Buy & hold: {benchmark_metrics[name]}",
            delta_color="off",
            delta_arrow="off",
            help=METRIC_HELP[name],
        )
    if len(prices) < 63:  # about 3 months of trading days
        st.caption(
            "⚠️ This window is shorter than about 3 months, so the annualised figures (CAGR, Sharpe) "
            "are unreliable: a few lucky days get scaled up to a whole year."
        )

    st.subheader(f"{ticker}: price and trades")
    st.pyplot(plot_signals(prices, result, overlays={k: v.loc[window] for k, v in overlays.items()}))
    st.caption(f"Black: the closing price. {rule} ▲ = buy, ▼ = sell, both at that day's close.")

    st.subheader("Portfolio value and drawdown")
    st.pyplot(plot_result(result))
    st.caption(
        "Top: what $10,000 would be worth. Bottom: drawdown, how far each portfolio is below its own previous "
        "high. A strategy can earn less than buy & hold and still be attractive if its drawdowns are much smaller."
    )

    st.subheader("Strategy vs buy & hold")
    st.dataframe(result.summary())
    st.caption(
        "Annual volatility: how much returns swing, scaled to a year. Number of trades: completed buy-then-sell "
        "round trips (plus one still open, if any). Win rate: the share of trades that made money."
    )

    st.subheader(f"Trades ({len(result.trades)})")
    trades_table = result.trades.copy()
    for column in ["entry_date", "exit_date"]:
        trades_table[column] = pd.to_datetime(trades_table[column]).dt.date  # drop the 00:00:00
    trades_table["return"] = trades_table["return"] * 100  # 0.12 -> 12, shown as "12.0%"
    st.dataframe(
        trades_table,
        hide_index=True,
        column_config={
            "entry_date": st.column_config.DateColumn("Entry", format="YYYY-MM-DD"),
            "exit_date": st.column_config.DateColumn("Exit", format="YYYY-MM-DD"),
            "direction": "Direction",
            "entry_price": st.column_config.NumberColumn("Entry price", format="%.2f"),
            "exit_price": st.column_config.NumberColumn("Exit price", format="%.2f"),
            "return": st.column_config.NumberColumn("Return", format="%.1f%%"),
            "open": st.column_config.CheckboxColumn("Still open"),
        },
    )
    st.caption(
        "Prices are closes on the signal day; returns are before costs. "
        "\"Still open\" means the position was still held when the data ended — it is valued at the last close."
    )
