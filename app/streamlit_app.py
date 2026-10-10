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
from backtester.plotting import plot_result, plot_signals
from strategies import ma_crossover, rsi_mean_reversion

st.set_page_config(page_title="Algo Trading Backtester", page_icon="📈", layout="wide")
st.title("📈 Algo trading backtester")
st.caption(
    "QM FinTech Society quant workshop · Educational use only — not financial advice. "
    "Price data from Yahoo Finance; no ownership is claimed."
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
else:
    if lower >= upper:
        st.warning("The buy level must be below the sell level — adjust the slider.")
        st.stop()
    positions = rsi_mean_reversion(full_history, period=period, lower=lower, upper=upper)
    overlays = {}

window = slice(pd.Timestamp(dates[0]), pd.Timestamp(dates[1]))
prices = full_history.loc[window]
if len(prices) < 2:
    st.warning("Pick a date range of at least two trading days.")
    st.stop()

result = run_backtest(prices, positions.loc[window], cost_bps=cost_bps)

strategy_metrics = format_metrics(result.metrics)
benchmark_metrics = format_metrics(result.benchmark_metrics)
for column, name in zip(st.columns(4), ["Total return", "Annual return (CAGR)", "Sharpe ratio", "Max drawdown"]):
    column.metric(name, strategy_metrics[name], f"Buy & hold: {benchmark_metrics[name]}", delta_color="off")

st.subheader(f"{ticker}: price and trades")
st.pyplot(plot_signals(prices, result, overlays={k: v.loc[window] for k, v in overlays.items()}))

st.subheader("Portfolio value and drawdown")
st.pyplot(plot_result(result))

left, right = st.columns(2)
left.subheader("Strategy vs buy & hold")
left.dataframe(result.summary())
right.subheader(f"Trades ({len(result.trades)})")
right.dataframe(result.trades)
