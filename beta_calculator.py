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

import pandas as pd
import numpy as np
from scipy.stats import linregress
import os
from matplotlib import pyplot as plt

# Path settings
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "DailyQuotes/{}.txt")

class InvalidTickersError(Exception):
    pass

def read_quotes(ticker):
    snp500_symbol = "^GSPC"
    stock_quotes_df = pd.read_csv(db_path.format(ticker), index_col="Date")
    snp_quotes_df = pd.read_csv(db_path.format(snp500_symbol), index_col="Date")

    quotes_date = stock_quotes_df.index
    stock_close_price = stock_quotes_df["Adj Close"]
    snp_close_price = snp_quotes_df["Adj Close"]

    return quotes_date, stock_close_price, snp_close_price

def beta_calc(quotes_date, stock_close_price, snp_close_price, ticker):
    stock_log_return = np.log(stock_close_price / stock_close_price.shift(1))
    snp_log_return = np.log(snp_close_price / snp_close_price.shift(1))

    cov_matrix = np.cov(stock_log_return[1:], snp_log_return[1:])
    # Covariance
    cov = cov_matrix[0,1]
    # Variance - S&P500
    var_snp = cov_matrix[1,1]
    # Variance - Stock
    # var_stock = cov_matrix[0,0]

    beta = round(cov / var_snp, 2)
    # print("Beta Coefficient: ", beta)

    # To calculate the regression line
    slope, intercept = linregress(snp_log_return[1:], stock_log_return[1:])[:2]

    # Drawing Chart
    p_obs = plt.plot([snp_log_return], [stock_log_return], "ro")
    p_regl = plt.plot(snp_log_return, intercept + slope * snp_log_return, "b")
    # Format axis as percent
    plt.gca().set_xticklabels(["{:.0f}%".format(x*100) for x in plt.gca().get_xticks()])
    plt.gca().set_yticklabels(["{:.0f}%".format(y*100) for y in plt.gca().get_yticks()])

    plt.title(f"Beta Chart\n(Beta Coefficient: {beta})")
    plt.ylabel(f"Stock ({ticker}) Return (%)")
    plt.xlabel("S&P 500 Index Return (%)")
    plt.legend((p_obs[0], p_regl[0]), ("Return Observations", "Regression Line"))
    plt.grid(True)
    plt.show()
    return beta

def run(ticker):
    val_tickers = ("AMAT", "C", "JD", "MSFT", "MU", "TWTR")
    try:

        ticker = str.upper(ticker)
        if ticker not in val_tickers:
            raise InvalidTickersError()

        quotes_date, stock_close_price, snp_close_price = read_quotes(ticker)
        beta = beta_calc(quotes_date, stock_close_price, snp_close_price, ticker)
        return beta

    except InvalidTickersError:
        print("[Error] Invalid ticker, please select one of them: (AMAT, C, JD, MSFT, MU, TWTR)")

if __name__ == "__main__":
    beta = run("MU")
