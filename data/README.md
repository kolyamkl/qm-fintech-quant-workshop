# Data

`prices.csv` holds **daily prices for 24 US ETFs and stocks** from **2016-01-04** to **2026-10-09** (64,992 rows, 3.7 MB), generated on 2026-10-10.

## Columns

| Column | Meaning |
|---|---|
| `Date` | Trading day (YYYY-MM-DD) |
| `Ticker` | Which instrument the row is about |
| `Open`, `High`, `Low`, `Close` | First, highest, lowest and last price of the day |
| `Volume` | Number of shares traded that day |

All prices are **adjusted for splits and dividends**, so a stock split doesn't look like a crash and returns already include dividends. That makes old prices look lower than what was actually traded at the time — e.g. AAPL in 2016 shows far below its real trading price then. Returns and backtests are correct; just don't use these numbers as the real historical price.

One row per ticker per day ("long" format). Load it with:

```python
from backtester import load_prices, load_closes
spy = load_prices("SPY")                      # one ticker
closes = load_closes(["SPY", "QQQ", "TLT"])   # closing prices side by side
```

## Tickers

| Group | Ticker | Name |
|---|---|---|
| Index ETFs | SPY | SPDR S&P 500 ETF (500 large US companies) |
| | QQQ | Invesco QQQ (Nasdaq-100) |
| | IWM | iShares Russell 2000 (small US companies) |
| | DIA | SPDR Dow Jones Industrial Average ETF |
| Sector ETFs | XLK | Technology |
| | XLF | Financials |
| | XLE | Energy |
| | XLV | Health Care |
| | XLY | Consumer Discretionary |
| | XLP | Consumer Staples |
| | XLI | Industrials |
| | XLU | Utilities |
| | XLB | Materials |
| Stocks | AAPL | Apple |
| | MSFT | Microsoft |
| | AMZN | Amazon |
| | GOOGL | Alphabet (Class A) |
| | JPM | JPMorgan Chase |
| | JNJ | Johnson & Johnson |
| | XOM | Exxon Mobil |
| | PG | Procter & Gamble |
| Bonds & gold | TLT | iShares 20+ Year Treasury Bond ETF |
| | IEF | iShares 7-10 Year Treasury Bond ETF |
| | GLD | SPDR Gold Shares |

## Source and disclaimer

Downloaded from **Yahoo Finance** with the [`yfinance`](https://github.com/ranaroussi/yfinance) library. Educational use only — not financial advice. Price data from Yahoo Finance; no ownership is claimed.

To rebuild or extend the file (e.g. different dates or tickers — edit `TICKERS` in the script):

```bash
python scripts/download_data.py
```
