"""
STOCK MARKET ANALYSIS DASHBOARD
================================
What this does:
  1. Downloads 1 year of price history for Apple, Tesla, HBL, and Meezan Bank
  2. Calculates daily returns, cumulative returns, and moving averages
  3. Pulls basic valuation metrics (P/E, market cap, etc.)
  4. Saves everything into one Excel file with charts, ready to open

HOW TO RUN THIS (no coding experience needed):
  1. Go to https://colab.research.google.com
  2. Click "New Notebook"
  3. Paste this ENTIRE script into the first cell
  4. Press Shift + Enter (or click the play button)
  5. Wait ~20-30 seconds. A file called "stock_dashboard.xlsx" will appear
     in the file panel on the left (click the folder icon to see it)
  6. Right-click it -> Download

A NOTE ON THE PAKISTANI STOCKS (HBL, Meezan Bank):
  Yahoo Finance's coverage of PSX (Pakistan Stock Exchange) tickers is
  inconsistent. This script tries the standard ".KA" suffix format
  (HBL.KA, MEBL.KA). If those come back empty, the script will tell you
  and skip them gracefully instead of crashing -- you can then check the
  PSX website directly for that data.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
# STEP 1: SETTINGS -- change these if you want different stocks/dates
# -------------------------------------------------------------------
TICKERS = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "HBL": "HBL.KA",
    "Meezan Bank": "MEBL.KA",
}
PERIOD = "1y"          # how far back: "6mo", "1y", "2y", "5y"
OUTPUT_FILE = "stock_dashboard.xlsx"

# -------------------------------------------------------------------
# STEP 2: DOWNLOAD DATA + CALCULATE METRICS FOR EACH STOCK
# -------------------------------------------------------------------
all_price_data = {}
valuation_rows = []

for company_name, ticker_symbol in TICKERS.items():
    print(f"Fetching {company_name} ({ticker_symbol})...")
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period=PERIOD)

    if history.empty:
        print(f"  -> No data found for {ticker_symbol}. Skipping.")
        continue

    # Keep only the columns we care about
    df = history[["Open", "High", "Low", "Close", "Volume"]].copy()

    # Daily return = % change from previous day
    df["Daily Return %"] = df["Close"].pct_change() * 100

    # Cumulative return = % growth since day 1
    df["Cumulative Return %"] = (df["Close"] / df["Close"].iloc[0] - 1) * 100

    # Moving averages -- smooth out the price to see the trend
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    df = df.round(2)
    df.index = df.index.tz_localize(None)  # remove timezone for Excel
    all_price_data[company_name] = df

    # Basic valuation metrics (from Yahoo's info dict -- not always complete)
    # NOTE: Yahoo's live "quote" data (info dict) is sometimes stale or wrong
    # for less-covered tickers like PSX stocks. The actual last closing price
    # from the historical data we already downloaded is more trustworthy, so
    # we use THAT for "Current Price" instead of info.get("currentPrice").
    info = ticker.info
    last_close_price = df["Close"].iloc[-1]

    # Yahoo's pre-calculated "dividendYield" field has switched formats
    # between library versions (sometimes a decimal like 0.0044, sometimes
    # a percent like 0.44) and there's no reliable way to detect which one
    # you got -- a guess-based threshold breaks for genuinely low-yield
    # stocks like Apple. Instead, we calculate the yield ourselves from the
    # actual annual dividend amount per share, which Yahoo reports
    # consistently in dollars/rupees (not a percentage), divided by price.
    dividend_rate = info.get("dividendRate")  # annual $ per share, e.g. 1.04
    if dividend_rate:
        dividend_pct = round((dividend_rate / last_close_price) * 100, 2)
    else:
        dividend_pct = None

    valuation_rows.append({
        "Company": company_name,
        "Ticker": ticker_symbol,
        "Current Price (last close)": round(last_close_price, 2),
        "Market Cap": info.get("marketCap"),
        "P/E Ratio (trailing)": info.get("trailingPE"),
        "P/E Ratio (forward)": info.get("forwardPE"),
        "P/B Ratio": info.get("priceToBook"),
        "52-Week High": info.get("fiftyTwoWeekHigh"),
        "52-Week Low": info.get("fiftyTwoWeekLow"),
        "Dividend Yield %": dividend_pct,
    })

valuation_df = pd.DataFrame(valuation_rows)

# Record exactly when this data was pulled, so anyone looking at the
# dashboard later knows it's a snapshot, not a live feed
generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
note_df = pd.DataFrame([{
    "Note": f"Data pulled from Yahoo Finance on {generated_at}. "
            f"This is a SNAPSHOT, not a live feed -- prices will be out of date "
            f"as soon as the market moves. Re-run this script for fresh numbers."
}])

# -------------------------------------------------------------------
# STEP 3: WRITE EVERYTHING TO ONE EXCEL FILE, ONE SHEET PER STOCK
#          PLUS A SUMMARY SHEET WITH VALUATION METRICS
# -------------------------------------------------------------------
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    note_df.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
    valuation_df.to_excel(writer, sheet_name="Summary", index=False, startrow=3)
    for company_name, df in all_price_data.items():
        # Excel sheet names can't be longer than 31 characters
        sheet_name = company_name[:31]
        df.to_excel(writer, sheet_name=sheet_name)

# -------------------------------------------------------------------
# STEP 4: ADD SIMPLE CHARTS (price + moving averages) TO EACH SHEET
# -------------------------------------------------------------------
from openpyxl import load_workbook
from openpyxl.chart import LineChart, Reference

wb = load_workbook(OUTPUT_FILE)

for company_name, df in all_price_data.items():
    sheet_name = company_name[:31]
    ws = wb[sheet_name]
    n_rows = len(df) + 1  # +1 for header row

    chart = LineChart()
    chart.title = f"{company_name}: Close Price vs Moving Averages"
    chart.y_axis.title = "Price"
    chart.x_axis.title = "Date"
    chart.width = 24
    chart.height = 10

    # Close price is column 5 (E), MA20 is column 8 (H), MA50 is column 9 (I)
    # (columns: A=Date, B=Open, C=High, D=Low, E=Close, F=Volume, G=Daily Return,
    #  H=Cumulative Return, I=MA20, J=MA50)
    close_col = df.columns.get_loc("Close") + 2   # +2: +1 for index col, +1 for 1-based
    ma20_col = df.columns.get_loc("MA20") + 2
    ma50_col = df.columns.get_loc("MA50") + 2

    for col in [close_col, ma20_col, ma50_col]:
        data_ref = Reference(ws, min_col=col, min_row=1, max_row=n_rows)
        chart.add_data(data_ref, titles_from_data=True)

    dates_ref = Reference(ws, min_col=1, min_row=2, max_row=n_rows)
    chart.set_categories(dates_ref)

    ws.add_chart(chart, f"L2")

wb.save(OUTPUT_FILE)
print(f"\nDone! '{OUTPUT_FILE}' has been created with {len(all_price_data)} stock sheets + a Summary sheet.")
print(f"Snapshot taken: {generated_at}")
print("Reminder: this data is NOT live. Re-run this script whenever you want fresh numbers.")
print("Download it from the file panel on the left in Colab.")
