# Take-home project: build your own trading dashboard

A web app that shows how an investment performed, how risky it was, and how much of its movement is just the market (CAPM). You build every number yourself, then publish the app for free.

**Start with the notebook:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kolyamkl/qm-fintech-quant-workshop/blob/main/notebooks/04_project_trading_dashboard.ipynb)

## What the finished app shows

- **Six headline numbers:** annual return, annual volatility, hit rate, Sharpe ratio, Sortino ratio and max drawdown.
- **Performance tab:** the growth of $1 and a rolling 63-day Sharpe ratio.
- **Risk tab:** drawdown and rolling 30-day volatility.
- **CAPM tab:** alpha, beta and R squared against a benchmark such as SPY.
- **Data tab:** the summary table and the prices.

## The files

```
analytics.py           ✏️ your calculations: copy your functions here from notebook 04
app.py                 ✏️ the web page, with five TODOs to fill in
checks.py              the ✅ / ❌ checks used by the notebook
solution/analytics.py  reference answers for every function
solution/app.py        the finished app
```

## Steps

1. Work through notebook `04_project_trading_dashboard` in Colab. Each step has a hint and a check.
2. Fork this repo on GitHub, then paste your functions into `analytics.py` (click the ✏️ pencil to edit a file in the browser).
3. At [share.streamlit.io](https://share.streamlit.io), click **Create app**, choose your fork, branch `main` and main file path `projects/trading_dashboard/app.py`, then click **Deploy**.
4. Fill in the TODOs in `app.py`. Every commit updates your live app.

The notebook's Part 2 has the full walkthrough and ideas to take it further.

On your own laptop instead (see the main README for the setup): `streamlit run projects/trading_dashboard/app.py`, or `streamlit run projects/trading_dashboard/solution/app.py` to see the finished version.
