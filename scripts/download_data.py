"""Rebuild data/prices.csv from Yahoo Finance.

You only need this if you want fresher data or different tickers — the repo
already ships with the file.

Usage:
    python scripts/download_data.py                              # 2016-01-01 to yesterday
    python scripts/download_data.py --start 2018-01-01 --end 2024-12-31

Prices are adjusted for splits and dividends (auto_adjust=True).
Data © Yahoo Finance — for educational use only.
"""

import argparse
import datetime as dt
from pathlib import Path

import pandas as pd

TICKERS = [
    # Broad index ETFs
    "SPY", "QQQ", "IWM", "DIA",
    # Sector ETFs
    "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB",
    # Large single stocks
    "AAPL", "MSFT", "AMZN", "GOOGL", "JPM", "JNJ", "XOM", "PG",
    # Bonds and gold
    "TLT", "IEF", "GLD",
]  # fmt: skip

DEFAULT_START = "2016-01-01"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "prices.csv"
PRICE_COLUMNS = ["Open", "High", "Low", "Close"]
COLUMNS = ["Date", "Ticker", *PRICE_COLUMNS, "Volume"]


def to_long_format(raw: pd.DataFrame) -> pd.DataFrame:
    """Turn yfinance's wide table (columns = (Price, Ticker)) into one row per ticker per day."""
    raw = raw.copy()
    raw.columns = raw.columns.set_names(["Price", "Ticker"])
    raw.index.name = "Date"

    frames = []
    for ticker in raw.columns.get_level_values("Ticker").unique():
        one = raw.xs(ticker, axis=1, level="Ticker").reset_index()
        one.insert(1, "Ticker", ticker)
        frames.append(one)
    long = pd.concat(frames, ignore_index=True)
    long.columns.name = None

    dates = pd.to_datetime(long["Date"])
    if dates.dt.tz is not None:
        dates = dates.dt.tz_localize(None)
    long["Date"] = dates.dt.normalize()

    long = long.dropna(subset=["Close"])  # days before a ticker existed
    long[PRICE_COLUMNS] = long[PRICE_COLUMNS].round(4)
    long["Volume"] = long["Volume"].fillna(0).astype("int64")
    return long[COLUMNS].sort_values(["Ticker", "Date"]).reset_index(drop=True)


def validate(df: pd.DataFrame, expected_tickers: list[str]) -> None:
    """Stop loudly if the data has gaps or duplicates."""
    missing = sorted(set(expected_tickers) - set(df["Ticker"]))
    if missing:
        raise ValueError(f"No data downloaded for: {missing}")
    if df[PRICE_COLUMNS].isna().any().any():
        raise ValueError("Found missing prices (NaN) — try downloading again.")
    duplicates = int(df.duplicated(["Date", "Ticker"]).sum())
    if duplicates:
        raise ValueError(f"Found {duplicates} duplicate (Date, Ticker) rows.")


def download(start: str, end: str | None) -> pd.DataFrame:
    import yfinance as yf  # only this script needs yfinance

    end = end or dt.date.today().isoformat()  # yfinance's end is exclusive -> up to yesterday
    raw = yf.download(TICKERS, start=start, end=end, auto_adjust=True, progress=False)
    return to_long_format(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--start", default=DEFAULT_START, help="first date, YYYY-MM-DD")
    parser.add_argument("--end", default=None, help="last date (exclusive), YYYY-MM-DD; default today")
    args = parser.parse_args()

    df = download(args.start, args.end)
    validate(df, TICKERS)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    size_mb = OUTPUT_PATH.stat().st_size / 1e6
    print(f"Wrote {len(df):,} rows for {df['Ticker'].nunique()} tickers to {OUTPUT_PATH} ({size_mb:.1f} MB)")
    print(f"Dates: {df['Date'].min():%Y-%m-%d} to {df['Date'].max():%Y-%m-%d}")


if __name__ == "__main__":
    main()
