"""YOUR STRATEGY HERE — copy this file, rename it, and make it your own.

A strategy is just a function:
    input:  prices — DataFrame with Open, High, Low, Close, Volume (from load_prices)
    output: a Series with one value per day:
              1 = hold the asset (long)
              0 = sit in cash
             -1 = bet against it (short)

Rules:
  * Only use information up to and including each day. The engine already
    waits one day before trading, so you don't need to shift anything yourself.
  * NaN is fine during warm-up (e.g. before a 200-day average exists) — it counts as 0.

Try it:
    from strategies.template import my_strategy
    from backtester import load_prices, run_backtest
    spy = load_prices("SPY")
    run_backtest(spy, my_strategy(spy)).summary()
"""

import pandas as pd


def my_strategy(prices: pd.DataFrame, lookback: int = 20) -> pd.Series:
    close = prices["Close"]

    # Ideas to get you started (uncomment one, or write your own):
    #   Momentum:  hold when the price is higher than `lookback` days ago
    #       position = (close > close.shift(lookback)).astype(int)
    #   Breakout:  hold when the price makes a new `lookback`-day high
    #       position = (close >= close.rolling(lookback).max()).astype(int)

    position = pd.Series(0, index=close.index)  # <- replace this line with your rule
    return position.rename("position")
