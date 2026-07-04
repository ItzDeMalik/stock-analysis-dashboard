# Stock Market Analysis Dashboard

A comparative analysis of Apple, Tesla, HBL, and Meezan Bank over a 12-month period. Historical market data was prepared using Python, while a standalone HTML dashboard visualizes the results through charts and key performance indicators..

**Live dashboard:** enable GitHub Pages (see below) and the link will be `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/dashboard.html`

## What's in this repo

| File | What it does |
|---|---|
| `stock_dashboard.py` | Downloads price history from Yahoo Finance, calculates returns/moving averages/valuation metrics, and exports everything to an Excel file |
| `dashboard.html` | A standalone visual dashboard (charts, KPI cards, insights) — open it in any browser, no installation needed |
| `stock_dashboard.xlsx` | The Excel output from the last time the script was run |

## ⚠ Dashboard Information

The dashboard displays a static snapshot of historical market data. Python was used to prepare the dataset, while the HTML dashboard presents the results. The dashboard does not automatically fetch live market data and must be regenerated manually when updated information is required.

## Updating the Dashboard

1. Go to [colab.research.google.com](https://colab.research.google.com) → New Notebook
2. Paste in the contents of `stock_dashboard.py`
3. Run it (Shift + Enter) — this downloads a fresh `stock_dashboard.xlsx`
4. Open `dashboard.html` in a text editor, find the section near the bottom marked:
   ```
   // DATA BLOCK — replace these arrays after re-running stock_dashboard.py
   ```
5. Replace the `dates`, `apple`, `tesla`, `hbl`, and `meezan` arrays with the new cumulative-return numbers from your fresh Excel file, and update the KPI cards (best return, lowest risk, etc.) near the top of the file if they've changed
6. Save, then re-upload both files to GitHub (see below)

## How to put this on GitHub (no coding experience needed)

1. Create a free account at [github.com](https://github.com) if you don't have one
2. Click the **+** icon top-right → **New repository**
3. Name it something like `stock-analysis-dashboard`, keep it **Public**, click **Create repository**
4. On the new repo page, click **uploading an existing file**
5. Drag in `stock_dashboard.py`, `dashboard.html`, `stock_dashboard.xlsx`, and this `README.md`
6. Click **Commit changes**

## How to make the dashboard viewable as a live webpage (GitHub Pages)

1. In your repo, go to **Settings** → **Pages** (left sidebar)
2. Under **Branch**, select `main` and folder `/ (root)`, then click **Save**
3. Wait about a minute, then refresh — GitHub will show you a link like:
   `https://YOUR-USERNAME.github.io/stock-analysis-dashboard/dashboard.html`
4. The link is now a shareable webpage displaying the latest generated version of the dashboard. The displayed data remains a static snapshot until the dataset is regenerated.

## Data & methodology

- **Source:** Yahoo Finance, accessed via the `yfinance` Python library
- **Period:** trailing 12 months
- **Metrics:** daily and cumulative returns, 20-day and 50-day moving averages, annualized volatility, trailing P/E, P/B ratio, 52-week range
- **Note on HBL and Meezan Bank:** these trade on the Pakistan Stock Exchange (PSX). Yahoo Finance's coverage of PSX tickers is less consistent than US tickers, so treat their figures as indicative.

This project is for educational purposes and is not financial advice.
