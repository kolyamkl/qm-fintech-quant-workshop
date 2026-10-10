import pandas as pd
import pytest

from strategies import ma_crossover, my_strategy, rsi, rsi_mean_reversion


def test_ma_crossover_is_flat_in_warmup_and_downtrend_then_long(make_prices):
    prices = make_prices(list(range(120, 110, -1)) + list(range(111, 121)))
    positions = ma_crossover(prices, fast=2, slow=5)
    assert positions.index.equals(prices.index)
    assert (positions.iloc[:10] == 0).all()  # warm-up + falling prices
    assert positions.iloc[-1] == 1  # rising prices: fast MA above slow MA


def test_ma_crossover_rejects_fast_not_below_slow(make_prices):
    prices = make_prices([100] * 10)
    with pytest.raises(ValueError, match="fast"):
        ma_crossover(prices, fast=5, slow=5)


def test_rsi_is_100_when_price_only_rises_and_0_when_it_only_falls():
    up = pd.Series(range(1, 40), dtype=float)
    down = pd.Series(range(40, 1, -1), dtype=float)
    assert rsi(up, 14).dropna().eq(100).all()
    assert rsi(down, 14).dropna().eq(0).all()
    assert rsi(up, 14).iloc[:14].isna().all()  # warm-up


def test_rsi_mean_reversion_buys_oversold_and_sells_overbought(make_prices):
    prices = make_prices(list(range(130, 100, -1)) + list(range(102, 132)))
    r = rsi(prices["Close"], 14)
    positions = rsi_mean_reversion(prices)
    first_buy = r[r < 30].index[0]
    first_sell = r[(r > 70) & (r.index > first_buy)].index[0]
    assert (positions.loc[:first_buy].iloc[:-1] == 0).all()
    assert (positions.loc[first_buy:first_sell].iloc[:-1] == 1).all()
    assert (positions.loc[first_sell:] == 0).all()


def test_rsi_mean_reversion_rejects_bad_levels(make_prices):
    prices = make_prices([100] * 30)
    with pytest.raises(ValueError, match="lower"):
        rsi_mean_reversion(prices, lower=50, upper=50)


def test_template_returns_flat_positions(make_prices):
    prices = make_prices([100, 101, 102])
    positions = my_strategy(prices)
    assert positions.index.equals(prices.index)
    assert (positions == 0).all()
