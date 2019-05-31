#!/usr/bin/python3

"""
-------------------------------------------------------------------
                CORRELATION COEFFICIENT CALCULATOR
-------------------------------------------------------------------

Calculates Correlation Coefficient, a measure of the historical
relationship between two stocks.

|
| Input parameter(s):   Ticker Symbol #1, Ticker Symbol #2
|                       eg. "AMAT", "MU"
|

Ticker Symbol:  Stock symbol from the 'Valid Ticker Symbols' list.
                Valid Ticker Symbols (AMAT, C, JD, MSFT, MU, TWTR)

Remark: Input parameters must be separated by comma(s).

-------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from datetime import datetime
import re

# Path settings
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

class InvalidTickersError(Exception):
    pass

def read_quotes(ticker1, ticker2):
    stock1_quotes_df = pd.read_csv(db_path.format(ticker1), index_col="Date")
    stock2_quotes_df = pd.read_csv(db_path.format(ticker2), index_col="Date")

    stock1_close_price = stock1_quotes_df["Adj Close"]
    stock2_close_price = stock2_quotes_df["Adj Close"]

    # Set proper date format for the Chart
    date_format = "%Y-%m-%d"
    quotes_date = [datetime.strptime(i, date_format) for i in stock1_quotes_df.index]
    quotes_date = matplotlib.dates.date2num(quotes_date)
    base_date = stock1_quotes_df.index[0]

    return base_date, quotes_date, stock1_close_price, stock2_close_price

def corr_calc(base_date, quotes_date, stock1_close_price, stock2_close_price, ticker1, ticker2):

    stock1_perf = list(map(lambda s: s / stock1_close_price[0] * 100, stock1_close_price))
    stock2_perf = list(map(lambda s: s / stock2_close_price[0] * 100, stock2_close_price))

    stock1_log_return = np.log(stock1_close_price / stock1_close_price.shift(1))
    stock2_log_return = np.log(stock2_close_price / stock2_close_price.shift(1))

    corr = round(np.corrcoef(stock1_log_return[1:], stock2_log_return[1:])[0, 1], 2)
    # print("Correlation Coefficient: ", corr)

    # Drawing Chart
    p_perf1 = plt.plot(quotes_date, stock1_perf, "b")
    p_perf2 = plt.plot(quotes_date, stock2_perf, "r")
    # Format "Date" axis
    plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    plt.title(f"{ticker1} vs. {ticker2} Performance\n(Correlation Coefficient: {corr})")
    plt.ylabel(f"Stock Price Rebased to 100 as of {base_date}")
    plt.xlabel("Date")
    plt.legend((p_perf1[0], p_perf2[0]), (ticker1, ticker2), loc=2)
    plt.grid(True)
    plt.show()
    return corr


def run(ticker1, ticker2):
    val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
    try:
        ticker1 = re.findall("\w+", str.upper(ticker1))[0]
        ticker2 = re.findall("\w+", str.upper(ticker2))[0]

        if ticker1 not in val_tickers or ticker2 not in val_tickers:
            raise InvalidTickersError()

        base_date, quotes_date, stock1_close, stock2_close = read_quotes(ticker1, ticker2)
        corr = corr_calc(base_date, quotes_date, stock1_close, stock2_close, ticker1, ticker2)
        return corr

    except InvalidTickersError:
        print("[Error] Invalid ticker, please select them from this list: (AMAT, C, JD, MSFT, MU, TWTR)")
