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


class InvalidTickersError(Exception):
    pass


class PeriodError(Exception):
    pass


class HVol:
    def __init__(self, ticker, period):
        self.ticker = ticker
        self.period = period
        # Path settings
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

    def read_quotes(self, symbol):
        return pd.read_csv(self.db_path.format(symbol), index_col="Date")

    @staticmethod
    def get_close_price(price_data_df):
        return price_data_df["Adj Close"]

    @staticmethod
    def get_quotes_date(stock_quotes_df):
        # Set proper date format for the Chart
        date_format = "%Y-%m-%d"
        quotes_date = [datetime.strptime(i, date_format) for i in stock_quotes_df.index]
        return matplotlib.dates.date2num(quotes_date)

    @staticmethod
    def calc_log_return(snp_quotes_df, stock_quotes_df):
        snp_close_price = HVol.get_close_price(snp_quotes_df)
        stock_close_price = HVol.get_close_price(stock_quotes_df)

        stock_log_return = np.log(stock_close_price / stock_close_price.shift(1))
        snp_log_return = np.log(snp_close_price / snp_close_price.shift(1))
        return snp_log_return, stock_log_return

    def calc_annual_hv_series(self, log_return):
        std_df = log_return.rolling(window=self.period, center=False).std(ddof=1)
        return np.sqrt(252) * std_df * 100

    @staticmethod
    def calc_annual_hv(ann_std_df):
        return "{0:.2f}%".format(ann_std_df.iloc[-1])

    def draw_chart(self, quotes_date, ann_stock_std_df, ann_stock_hv, \
                   ann_snp_std_df, ann_snp_hv):
        # Drawing Chart
        p_hv1 = plt.plot(quotes_date, ann_stock_std_df, "b")
        p_hv2 = plt.plot(quotes_date, ann_snp_std_df, "r")
        # Format "Date" axis
        plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        plt.title(f"{self.ticker} vs. S&P 500 Index Historical Volatility\n"
                  f"(Stock HV: {ann_stock_hv} | Index HV: {ann_snp_hv} | Period: {self.period})")
        plt.ylabel("Annual Historical Volatility (%)")
        plt.xlabel("Date")
        plt.legend((p_hv1[0], p_hv2[0]), (self.ticker, "S&P 500 Index"), loc=2)
        plt.grid(True)
        plt.show()

    def run_app(self):
        # There are pricing data for the followings
        val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
        try:
            if self.ticker not in val_tickers:
                raise InvalidTickersError()

            elif not float(self.period).is_integer():
                raise PeriodError()

            elif float(self.period) < 2 or float(self.period) >= 100:
                raise PeriodError()

            snp_quotes_df = self.read_quotes("^GSPC")
            stock_quotes_df = self.read_quotes(self.ticker)
            snp_log_return, stock_log_return \
                        = HVol.calc_log_return(snp_quotes_df, stock_quotes_df)
            ann_snp_std_df = self.calc_annual_hv_series(snp_log_return)
            ann_stock_std_df = self.calc_annual_hv_series(stock_log_return)
            ann_snp_hv = HVol.calc_annual_hv(ann_snp_std_df)
            ann_stock_hv = HVol.calc_annual_hv(ann_stock_std_df)
            quotes_date = HVol.get_quotes_date(stock_quotes_df)
            self.draw_chart(quotes_date, ann_stock_std_df, ann_stock_hv, \
                            ann_snp_std_df, ann_snp_hv)
            return ann_stock_hv, ann_snp_hv

        except InvalidTickersError:
            print("[Error] Invalid ticker, please select one of them: (AMAT, C, JD, MSFT, MU, TWTR)")
        except PeriodError:
            print("[Error] Period must be integer, greater than 1 and less than 100")


if __name__ == "__main__":
    hv = HVol("MU", 30)
    hv.run_app()
