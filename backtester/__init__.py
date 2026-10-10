"""A tiny, readable backtesting engine for the QM FinTech Society quant workshop."""

from .data import available_tickers, load_closes, load_prices
from .engine import BacktestResult, run_backtest

__all__ = ["BacktestResult", "available_tickers", "load_closes", "load_prices", "run_backtest"]
