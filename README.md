# QM FinTech Quant Workshop: Algorithmic Trading

A beginner-friendly starter kit for **backtesting trading strategies in Python** — real market data, a small engine you can read in one sitting, worked notebooks, an interactive app, and resources to keep going.

Led by **Adnan Salehin** (Lead SWE & VP, JPMorgan) · Organised by **QM FinTech Society**

> Educational use only — not financial advice. Price data from Yahoo Finance; no ownership is claimed.

---

## Start here — pick one

| Option | Best for | How |
|---|---|---|
| 🌐 **Hosted app** | Just exploring, no code | *Link coming before the workshop* |
| ☁️ **Google Colab** | Coding without installing anything | Click a badge below |
| 💻 **Your laptop** | Building your own strategies | See [Local setup](#local-setup) |

| Notebook | What it covers | Colab |
|---|---|---|
| `00_intro_to_algo_trading` | What algo trading is + key terms | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kolyamkl/qm-fintech-quant-workshop/blob/main/notebooks/00_intro_to_algo_trading.ipynb) |
| `01_workshop_ma_crossover` | **The main workshop**: data → signal → backtest → pitfalls | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kolyamkl/qm-fintech-quant-workshop/blob/main/notebooks/01_workshop_ma_crossover.ipynb) |
| `02_rsi_mean_reversion` | A second strategy: buy the dip, sell the rip | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kolyamkl/qm-fintech-quant-workshop/blob/main/notebooks/02_rsi_mean_reversion.ipynb) |
| `03_compare_with_library` | The same strategy in backtesting.py | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kolyamkl/qm-fintech-quant-workshop/blob/main/notebooks/03_compare_with_library.ipynb) |

## Workshop agenda (~1.5–2 hours)

| Part | Time |
|---|---|
| Intro: what is algorithmic trading? (`00`) | 10–15 min |
| Build and backtest a moving-average crossover (`01`) | ~60 min |
| Demo: the interactive app | ~10 min |
| If time allows: RSI mean reversion (`02`) | remaining |
| Q&A | ~10 min |

## Local setup

You need **Python 3.11 or newer** ([python.org/downloads](https://www.python.org/downloads/)) and **git**.

```bash
git clone https://github.com/kolyamkl/qm-fintech-quant-workshop.git
cd qm-fintech-quant-workshop
python -m venv .venv
```

Activate the environment:

- **macOS / Linux:** `source .venv/bin/activate`
- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (cmd):** `.venv\Scripts\activate.bat`

Then install and run:

```bash
pip install -r requirements.txt
jupyter lab                         # opens the notebooks in your browser
streamlit run app/streamlit_app.py  # opens the interactive app
```

(On macOS you may need `python3` instead of `python`.)

## Write your own strategy in 3 steps

A strategy is just a function: prices in, positions out (`1` = hold, `0` = cash, `-1` = short).

1. Copy `strategies/template.py` to e.g. `strategies/my_idea.py`.
2. Replace the marked line with your rule.
3. Backtest it:

```python
from backtester import load_prices, run_backtest
from strategies.my_idea import my_strategy

spy = load_prices("SPY")
result = run_backtest(spy, my_strategy(spy), cost_bps=5)
result.summary()   # strategy vs buy-and-hold
result.plot()      # portfolio value and drawdown
```

## What's in the repo

```
data/prices.csv        daily prices, 24 US ETFs & stocks, 2016 → 2026 (see data/README.md)
backtester/            the engine: data loading, run_backtest, metrics, charts
strategies/            ma_crossover, rsi_mean_reversion, and template.py for your own
notebooks/             the workshop, step by step
app/streamlit_app.py   interactive backtester
docs/glossary.md       every term, explained in a sentence
docs/resources.md      exercises, reading list, careers and interview prep
scripts/download_data.py   rebuilds data/prices.csv from Yahoo Finance
tests/                 checks that the engine computes correctly (run: pytest)
```

## How the engine works (in one paragraph)

`run_backtest` takes your daily positions, **shifts them by one day** (a decision made at today's close can only earn tomorrow's return — skipping this is the classic *look-ahead bias*), multiplies by the asset's daily returns, subtracts a trading cost whenever the position changes, and compounds the result from $10,000. Everything is compared with simply buying and holding. It deliberately leaves out slippage, position sizing and multi-asset portfolios — those are exercises in [`docs/resources.md`](docs/resources.md).

## Licence

Code: [MIT](LICENSE). Data: see [`data/README.md`](data/README.md).
