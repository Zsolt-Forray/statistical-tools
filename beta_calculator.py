#!/usr/bin/python3


"""
-------------------------------------------------------------------------------
                                BETA CALCULATOR
-------------------------------------------------------------------------------

Calculates 'Beta', a measure of a stock's volatility in relation to the market.

|
| Input parameter(s):   Ticker Symbol
|                       eg. "AMAT"
|

Ticker Symbol:  Stock symbol from the 'Valid Ticker Symbols' list.
                Valid Ticker Symbols (AMAT, C, JD, MSFT, MU, TWTR)

Remark: Input parameters must be separated by comma(s).

-------------------------------------------------------------------------------
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '27/11/2019'
__status__  = 'Development'


import pandas as pd
import numpy as np
from scipy.stats import linregress
import os
from matplotlib import pyplot as plt


class InvalidTickersError(Exception):
    pass


class Beta:
    def __init__(self, ticker):
        self.ticker = ticker
        # Path settings
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

    def read_quotes(self, symbol):
        return pd.read_csv(self.db_path.format(symbol), index_col="Date")

    @staticmethod
    def get_close_price(price_data_df):
        return price_data_df["Adj Close"]

    def calc_log_return(self):
        snp_quotes_df = self.read_quotes("^GSPC")
        stock_quotes_df = self.read_quotes(self.ticker)

        snp_close_price = get_close_price(snp_quotes_df)
        stock_close_price = get_close_price(stock_quotes_df)

        stock_log_return = np.log(stock_close_price / stock_close_price.shift(1))
        snp_log_return = np.log(snp_close_price / snp_close_price.shift(1))
        return snp_log_return, stock_log_return

    @staticmethod
    def calc_beta(snp_log_return, stock_log_return):
        cov_matrix = np.cov(stock_log_return[1:], snp_log_return[1:])
        # Covariance
        cov = cov_matrix[0,1]
        # Variance - S&P500
        var_snp = cov_matrix[1,1]
        # Variance - Stock
        # var_stock = cov_matrix[0,0]
        beta = round(cov / var_snp, 2)
        return beta

    @staticmethod
    def calc_regression_line(snp_log_return, stock_log_return):
        # To calculate the regression line
        slope, intercept = linregress(snp_log_return[1:], stock_log_return[1:])[:2]
        return slope, intercept

    def draw_chart(self, snp_log_return, stock_log_return, slope, intercept, beta):
        # Drawing Chart
        p_obs = plt.plot([snp_log_return], [stock_log_return], "ro")
        p_regl = plt.plot(snp_log_return, intercept + slope * snp_log_return, "b")
        # Format axis as percent
        plt.gca().set_xticklabels(["{:.0f}%".format(x*100) for x in plt.gca().get_xticks()])
        plt.gca().set_yticklabels(["{:.0f}%".format(y*100) for y in plt.gca().get_yticks()])

        plt.title("Beta Chart\n(Beta Coefficient: {})".format(beta))
        plt.ylabel(f"Stock ({self.ticker}) Return (%)")
        plt.xlabel("S&P 500 Index Return (%)")
        plt.legend((p_obs[0], p_regl[0]), ("Return Observations", "Regression Line"))
        plt.grid(True)
        plt.show()

    def run_app(self):
        # There are pricing data for the followings
        val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
        try:
            if self.ticker not in val_tickers:
                raise InvalidTickersError()

            snp_log_return, stock_log_return = self.calc_log_return()
            beta = calc_beta(snp_log_return, stock_log_return)
            slope, intercept = calc_regression_line(snp_log_return, stock_log_return)
            self.draw_chart(snp_log_return, stock_log_return, slope, intercept, beta)
            return beta

        except InvalidTickersError:
            print("[Error] Invalid ticker, please select one of them: (AMAT, C, JD, MSFT, MU, TWTR)")


if __name__ == "__main__":
    beta = Beta("C")
    beta.run_app()
