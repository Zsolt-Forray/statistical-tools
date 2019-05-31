#!/usr/bin/python3

"""
---------------------------------------------------------------------------
                    HISTORICAL VOLATILITY CALCULATOR
---------------------------------------------------------------------------

Calculates Historical Volatility, a statistical measure of the dispersion
of returns for a given security over a given period of time.

|
| Input parameter(s):   Ticker Symbol, Period
|                       eg. "AMAT", 30
|

Ticker Symbol:  Stock symbol from the 'Valid Ticker Symbols' list.
                Valid Ticker Symbols (AMAT, C, JD, MSFT, MU, TWTR)

Period must be integer between 2 and 99

Remark: Input parameters must be separated by comma(s).

---------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from datetime import datetime

# Path settings
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

class InvalidTickersError(Exception):
    pass

class PeriodError(Exception):
    pass

def read_quotes(ticker):
    snp500_symbol = "^GSPC"
    stock_quotes_df = pd.read_csv(db_path.format(ticker), index_col="Date")
    snp_quotes_df = pd.read_csv(db_path.format(snp500_symbol), index_col="Date")

    stock_close_price = stock_quotes_df["Adj Close"]
    snp_close_price = snp_quotes_df["Adj Close"]

    # Set proper date format for the Chart
    date_format = "%Y-%m-%d"
    quotes_date = [datetime.strptime(i, date_format) for i in stock_quotes_df.index]
    quotes_date = matplotlib.dates.date2num(quotes_date)

    return quotes_date, stock_close_price, snp_close_price

def hv_calc(quotes_date, stock_close_price, snp_close_price, period, ticker):
    # Stock
    stock_log_return = np.log(stock_close_price / stock_close_price.shift(1))
    stock_std_df = stock_log_return.rolling(window=period, center=False).std(ddof=1)
    ann_stock_std_df = np.sqrt(252) * stock_std_df * 100
    ann_stock_hv = "{0:.2f}%".format(ann_stock_std_df.iloc[-1])

    # S&P 500 Index
    snp_log_return = np.log(snp_close_price / snp_close_price.shift(1))
    snp_std_df = snp_log_return.rolling(window=period, center=False).std(ddof=1)
    ann_snp_std_df = np.sqrt(252) * snp_std_df * 100
    ann_snp_hv = "{0:.2f}%".format(ann_snp_std_df.iloc[-1])

    # print("Stock Annual Volatility: ", ann_stock_hv)
    # print("S&P 500 Annual Volatility: ", ann_snp_hv)

    # Drawing Chart
    p_hv1 = plt.plot(quotes_date, ann_stock_std_df, "b")
    p_hv2 = plt.plot(quotes_date, ann_snp_std_df, "r")
    # Format "Date" axis
    plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    plt.title(f"{ticker} vs. S&P 500 Index Historical Volatility\n" +
            f"(Stock HV: {ann_stock_hv} | Index HV: {ann_snp_hv} | Period: {period})")
    plt.ylabel("Annual Historical Volatility (%)")
    plt.xlabel("Date")
    plt.legend((p_hv1[0], p_hv2[0]), (ticker, "S&P 500 Index"), loc=2)
    plt.grid(True)
    plt.show()
    return tuple((ann_stock_hv, ann_snp_hv))


def run(ticker, period):
    val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
    try:

        ticker = str.upper(ticker)

        if ticker not in val_tickers:
            raise InvalidTickersError()

        elif float(period).is_integer() == False:
            raise PeriodError()

        elif float(period) < 2 or float(period) >= 100:
            raise PeriodError()

        period = int(period)
        quotes_date, stock_close_price, snp_close_price = read_quotes(ticker)
        ann_stock_hv, ann_snp_hv = hv_calc(quotes_date, stock_close_price, snp_close_price, period, ticker)
        return tuple((ann_stock_hv, ann_snp_hv))

    except InvalidTickersError:
        print("[Error] Invalid ticker, please select one of them: (AMAT, C, JD, MSFT, MU, TWTR)")
    except PeriodError:
        print("[Error] Period must be integer, greater than 1 and less than 100")
