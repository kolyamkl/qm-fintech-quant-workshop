# Glossary

Plain-English definitions of the terms used in this workshop, A–Z.

| Term | Meaning |
|---|---|
| **Adjusted price** | Price history rewritten so stock splits and dividends don't appear as fake jumps; use it for returns and backtests. |
| **Alpha** | Return a strategy earns beyond what its market exposure explains — the "skill" part. |
| **Backtest** | A simulation of how a strategy would have performed on historical data. |
| **Basis point (bp)** | One hundredth of a percent (0.01%). 5 bps = 0.05%. |
| **Bear / bull market** | A falling (bear) or rising (bull) market over a sustained period. |
| **Benchmark** | What you compare a strategy against — in this repo, buying and holding the same asset. |
| **Beta** | How strongly something moves with the market: a beta of 1.2 means it tends to move 1.2% when the market moves 1%. |
| **Bid / ask spread** | The gap between the highest price buyers offer (bid) and the lowest price sellers accept (ask); a hidden cost of every trade. |
| **CAGR** | Compound annual growth rate: the steady yearly return that would produce the same final result. |
| **CAPM** | Capital Asset Pricing Model: splits an investment's return into a market-driven part (beta) and what's left over (alpha). |
| **Death cross / golden cross** | The short moving average crossing below (death) or above (golden) the long one. |
| **Drawdown** | How far a portfolio is below its previous peak; **max drawdown** is the worst such fall. |
| **Equity curve** | A chart of portfolio value over time. |
| **ETF** | Exchange-traded fund: a single ticker holding a basket of assets, traded like a stock. |
| **Hit rate** | The share of days (or periods) with a positive return. |
| **Index** | A number tracking a group of assets, such as the S&P 500; ETFs like SPY track indices. |
| **Leverage** | Using borrowed money to hold positions bigger than your capital; magnifies both gains and losses. |
| **Liquidity** | How easily you can trade without moving the price; highly liquid assets have tight spreads. |
| **Long** | Owning an asset so you profit if its price rises. |
| **Look-ahead bias** | Using information in a backtest that wasn't available at the time of the decision. |
| **Market maker** | A firm that continuously quotes buy and sell prices and earns the spread. |
| **Mean reversion** | The idea that prices which moved unusually far tend to move back toward their average. |
| **Momentum** | The idea that assets which rose recently tend to keep rising for a while. |
| **Moving average (MA)** | The average of the last N closing prices; smooths out day-to-day noise. |
| **OHLCV** | Open, High, Low, Close, Volume — the five numbers summarising one trading period. |
| **Order (market / limit)** | An instruction to trade: a market order trades now at the best price; a limit order only at your price or better. |
| **Overfitting** | Tuning a strategy so closely to past data that it captures noise and fails on new data. |
| **Paper trading** | Running a strategy on live prices with fake money. |
| **Position** | What you currently hold: long, short, or flat (cash). |
| **R squared** | How much of an investment's movement the market explains, from 0% to 100%. |
| **Return** | Percentage change in value: from 100 to 105 is +5%. |
| **Risk-free rate** | The return on a (near) riskless investment such as short-term government bills; this repo assumes 0 for simplicity. |
| **RSI** | Relative Strength Index: a 0–100 score of recent price moves; below 30 "oversold", above 70 "overbought". |
| **Sector** | A group of companies in the same industry, e.g. technology (XLK) or energy (XLE). |
| **Sharpe ratio** | Average return divided by its volatility (annualised); higher means more return per unit of risk. |
| **Short** | Borrowing and selling an asset so you profit if its price falls. |
| **Signal** | The output of your rules telling you which position to hold. |
| **Slippage** | The difference between the price you expected and the price you actually got. |
| **Sortino ratio** | Like the Sharpe ratio, but only downside volatility (the bad days) counts as risk. |
| **Stop-loss** | A rule that exits a position once losses reach a set level. |
| **Strategy** | A complete set of rules turning data into positions. |
| **Survivorship bias** | Testing only on assets that still exist today, ignoring ones that failed or were delisted. |
| **Tearsheet** | A one-page summary of an investment's performance and risk. |
| **Ticker** | The short code identifying a tradable asset, e.g. SPY, AAPL. |
| **Transaction costs** | Fees, spreads and slippage paid on each trade. |
| **Trend following** | Buying assets that are rising and selling ones that are falling, betting the move continues. |
| **Volatility** | How much returns vary; the most common measure of risk. |
| **Volume** | The number of shares traded in a period. |
| **Walk-forward testing** | Repeatedly tuning on one period and testing on the next, rolling forward through time. |
| **Win rate** | The share of trades that made money. A high win rate doesn't guarantee profit — size of wins vs losses matters too. |
