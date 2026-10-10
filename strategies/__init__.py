"""Example trading strategies. Each is a function: prices -> positions (1 / 0 / -1)."""

from .ma_crossover import ma_crossover
from .rsi_mean_reversion import rsi, rsi_mean_reversion
from .template import my_strategy

__all__ = ["ma_crossover", "my_strategy", "rsi", "rsi_mean_reversion"]
