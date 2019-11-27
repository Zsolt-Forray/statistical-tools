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


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '27/11/2019'
__status__  = 'Development'


import pandas as pd
import numpy as np
import os
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from datetime import datetime
import re


class InvalidTickersError(Exception):
    pass


class Correlation:
    def __init__(self, ticker1, ticker2):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        # Path settings
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

    def read_quotes(self, symbol):
        return pd.read_csv(self.db_path.format(symbol), index_col="Date")

    def get_close_price(self, price_data_df):
        return price_data_df["Adj Close"]

    def get_quotes_date(self, stock1_quotes_df):
        # Set proper date format for the Chart
        date_format = "%Y-%m-%d"
        quotes_date = [datetime.strptime(i, date_format) for i in stock1_quotes_df.index]
        return matplotlib.dates.date2num(quotes_date)

    def get_base_date(self, stock1_quotes_df):
        return stock1_quotes_df.index[0]

    def calc_close_price(self, stock1_quotes_df, stock2_quotes_df):
        stock1_close_price = self.get_close_price(stock1_quotes_df)
        stock2_close_price = self.get_close_price(stock2_quotes_df)
        return stock1_close_price, stock2_close_price

    def calc_performance(self, stock1_close_price, stock2_close_price):
        stock1_perf = list(map(lambda s: s / stock1_close_price[0] * 100, stock1_close_price))
        stock2_perf = list(map(lambda s: s / stock2_close_price[0] * 100, stock2_close_price))
        return stock1_perf, stock2_perf

    def calc_log_return(self, stock1_close_price, stock2_close_price):
        stock1_log_return = np.log(stock1_close_price / stock1_close_price.shift(1))
        stock2_log_return = np.log(stock2_close_price / stock2_close_price.shift(1))
        return stock1_log_return, stock2_log_return

    def calc_correlation(self, stock1_log_return, stock2_log_return):
        return round(np.corrcoef(stock1_log_return[1:], stock2_log_return[1:])[0, 1], 2)

    def draw_chart(self, quotes_date, base_date, stock1_perf, stock2_perf, correlation):
        # Drawing Chart
        p_perf1 = plt.plot(quotes_date, stock1_perf, "b")
        p_perf2 = plt.plot(quotes_date, stock2_perf, "r")
        # Format "Date" axis
        plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        plt.title(f"{self.ticker1} vs. {self.ticker2} Performance\n"
                  f"(Correlation Coefficient: {correlation})")
        plt.ylabel(f"Stock Price Rebased to 100 as of {base_date}")
        plt.xlabel("Date")
        plt.legend((p_perf1[0], p_perf2[0]), (self.ticker1, self.ticker2), loc=2)
        plt.grid(True)
        plt.show()

    def run_app(self):
        # There are pricing data for the followings
        val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
        try:
            if self.ticker1 not in val_tickers or self.ticker2 not in val_tickers:
                raise InvalidTickersError()

            stock1_quotes_df = self.read_quotes(self.ticker1)
            stock2_quotes_df = self.read_quotes(self.ticker2)
            stock1_close_price, stock2_close_price \
                    = self.calc_close_price(stock1_quotes_df, stock2_quotes_df)
            stock1_perf, stock2_perf \
                    = self.calc_performance(stock1_close_price, stock2_close_price)
            stock1_log_return, stock2_log_return \
                    = self.calc_log_return(stock1_close_price, stock2_close_price)
            correlation = self.calc_correlation(stock1_log_return, stock2_log_return)
            quotes_date = self.get_quotes_date(stock1_quotes_df)
            base_date = self.get_base_date(stock1_quotes_df)
            self.draw_chart(quotes_date, base_date, stock1_perf, stock2_perf, correlation)
            return correlation

        except InvalidTickersError:
            print("[Error] Invalid ticker, please select one of them: (AMAT, C, JD, MSFT, MU, TWTR)")


if __name__ == "__main__":
    corr = Correlation("MU", "C")
    corr.run_app()
