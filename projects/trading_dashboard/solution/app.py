"""Trading dashboard: reference solution.

Run it locally from the repo folder:
    streamlit run projects/trading_dashboard/solution/app.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent.parent))  # repo root, for `backtester`
sys.path.insert(0, str(HERE))  # analytics.py next to this file

import analytics
import pandas as pd
import streamlit as st

from backtester import available_tickers, load_prices

HELP = {
    "Annual return": "The steady yearly growth rate (CAGR) that gives the same total result.",
    "Annual volatility": "How much daily returns swing, scaled to a year. Higher = bumpier ride.",
    "Hit rate": "The share of days that ended up.",
    "Sharpe ratio": "Return per unit of risk (risk-free rate taken as 0). Higher is better.",
    "Sortino ratio": "Like Sharpe, but only the down days count as risk.",
    "Max drawdown": "The worst fall from a previous high.",
}
PERCENT = {"Annual return", "Annual volatility", "Hit rate", "Max drawdown"}


def show(column, name, value):
    column.metric(name, f"{value:.1%}" if name in PERCENT else f"{value:.2f}", help=HELP[name])


st.set_page_config(page_title="Trading Dashboard", page_icon="📊", layout="wide")
st.title("📊 Trading dashboard")
st.caption("Performance and risk of one ticker, and how it moves with the market. Educational use only.")

tickers = available_tickers()
with st.sidebar:
    st.header("Settings")
    ticker = st.selectbox("Ticker to analyse", tickers, index=tickers.index("AAPL"))
    benchmark_ticker = st.selectbox("Benchmark (the market)", tickers, index=tickers.index("SPY"))

prices = load_prices(ticker)["Close"]
returns = analytics.to_returns(prices)
equity = analytics.equity_curve(returns)
stats = analytics.tearsheet(prices)

for row in (["Annual return", "Annual volatility", "Hit rate"], ["Sharpe ratio", "Sortino ratio", "Max drawdown"]):
    for column, name in zip(st.columns(3), row):
        show(column, name, stats[name])

performance, risk, capm_tab, data_tab = st.tabs(["Performance", "Risk", "CAPM", "Data"])

with performance:
    st.subheader("Equity curve: growth of $1")
    st.line_chart(equity)
    st.subheader("Rolling Sharpe ratio (63 days)")
    st.line_chart(analytics.rolling_sharpe(returns))
    st.caption("The Sharpe ratio of the last 63 trading days (about 3 months). It shows when the ride was good or bad.")

with risk:
    st.subheader("Drawdown")
    st.area_chart(analytics.drawdown(equity))
    st.caption("How far below its previous high the investment was each day. 0 means a new high.")
    st.subheader("Rolling volatility (30 days)")
    st.line_chart(analytics.rolling_volatility(returns))

with capm_tab:
    benchmark_returns = analytics.to_returns(load_prices(benchmark_ticker)["Close"])
    result = analytics.capm(returns, benchmark_returns)
    alpha, beta, r_squared = st.columns(3)
    alpha.metric("Alpha (per year)", f"{result['Alpha']:.1%}")
    beta.metric("Beta", f"{result['Beta']:.2f}")
    r_squared.metric("R squared", f"{result['R squared']:.0%}")
    st.markdown(
        f"**Beta** {result['Beta']:.2f}: on a day {benchmark_ticker} moves 1%, {ticker} tends to move "
        f"{result['Beta']:.2f}%. **Alpha** is the yearly return left over once that market part is "
        f"taken out. **R squared** is how much of {ticker}'s daily movement the market explains."
    )

with data_tab:
    st.subheader("Summary")
    st.dataframe(pd.Series(stats, name="Value").to_frame())
    st.subheader("Prices")
    st.dataframe(prices)
