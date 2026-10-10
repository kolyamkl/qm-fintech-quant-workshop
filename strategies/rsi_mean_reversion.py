"""RSI mean reversion — buy the dip, sell the rip.

The idea (mean reversion): prices that fall unusually fast tend to bounce back.
RSI (Relative Strength Index) scores recent moves from 0 to 100:
    below 30  -> "oversold"  (fell a lot recently)   -> buy
    above 70  -> "overbought" (rose a lot recently)  -> sell
In between we keep whatever position we already had.

This is the opposite bet to the moving-average crossover, which follows trends.
"""

import pandas as pd


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (0-100) using Wilder's smoothing."""
    change = close.diff()
    gains = change.clip(lower=0)  # up moves, 0 on down days
    losses = -change.clip(upper=0)  # down moves as positive numbers, 0 on up days

    # Wilder's smoothing is an exponential moving average with alpha = 1/period.
    avg_gain = gains.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = losses.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    relative_strength = avg_gain / avg_loss  # no losses at all -> infinity -> RSI 100
    return 100 - 100 / (1 + relative_strength)


def rsi_mean_reversion(prices: pd.DataFrame, period: int = 14, lower: float = 30, upper: float = 70) -> pd.Series:
    """Positions: buy when RSI drops below `lower`, sell when it rises above `upper`."""
    if not 0 < lower < upper < 100:
        raise ValueError(f"Need 0 < lower < upper < 100, got lower={lower}, upper={upper}.")

    r = rsi(prices["Close"], period)

    position = pd.Series(float("nan"), index=prices.index)
    position[r < lower] = 1  # oversold -> get in
    position[r > upper] = 0  # overbought -> get out
    # Days in between: carry the last decision forward. Before any signal: cash.
    return position.ffill().fillna(0).rename("position")
