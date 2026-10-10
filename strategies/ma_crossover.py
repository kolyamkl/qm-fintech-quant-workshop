"""Moving-average crossover — the classic first trading strategy.

The idea (trend following): when the short-term average price rises above the
long-term average, the price is trending up, so we buy. When it falls back below,
the trend has faded, so we sell and sit in cash.

    fast MA > slow MA  ->  1 (hold the asset)
    otherwise          ->  0 (cash)

The moment the fast MA crosses above the slow one is called a "golden cross";
crossing below is a "death cross".
"""

import pandas as pd


def ma_crossover(prices: pd.DataFrame, fast: int = 50, slow: int = 200) -> pd.Series:
    """Positions for a moving-average crossover strategy.

    prices: DataFrame with a "Close" column (e.g. from load_prices).
    fast:   length of the short moving average, in days.
    slow:   length of the long moving average, in days.
    """
    if not 1 <= fast < slow:
        raise ValueError(f"Need 1 <= fast < slow, got fast={fast}, slow={slow}.")

    close = prices["Close"]
    fast_ma = close.rolling(fast).mean()  # average of the last `fast` closes
    slow_ma = close.rolling(slow).mean()  # average of the last `slow` closes

    # While slow_ma is still warming up it is NaN, and NaN > x is False -> 0 (cash).
    return (fast_ma > slow_ma).astype(int).rename("position")
