# statistical-tools

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3885370dc5344aeba98c088256d4865f)](https://www.codacy.com/app/forray.zsolt/statistical-tools?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Zsolt-Forray/statistical-tools&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/3885370dc5344aeba98c088256d4865f)](https://www.codacy.com/app/forray.zsolt/statistical-tools?utm_source=github.com&utm_medium=referral&utm_content=Zsolt-Forray/statistical-tools&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/Zsolt-Forray/statistical-tools.svg?branch=master)](https://travis-ci.com/Zsolt-Forray/statistical-tools)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Description
This project includes different statistical measures (Beta and Historical Volatility) to quantify risk and Correlation Coefficient that is used for the mitigation of risk arising from equity selection.

- [Beta](#beta-calculator)
- [Historical Volatility](#historical-volatility-calculator)
- [Correlation Coefficient](#correlation-coefficient-calculator)

## Usage
1.  Create a new directory somewhere.
2.  Open the Start Menu, type `cmd` in the search field, and then press Enter.
3.  Clone the project by running (make sure that you are in the newly created directory first!):
```
git clone https://github.com/Zsolt-Forray/statistical-tools.git
```
4.  Tools are found in the `statistical-tools` folder.
5.  Import the selected tool.

Note:  
This project uses sample stock quotes from the `DailyQuotes` folder. If you want, you can add other stock quotes to this folder. If you add stock quotes having different timeframe, do not forget to update the other quotes accordingly.

Available quotes:  
+   Applied Materials (AMAT)
+   Citigroup (C)
+   JD.com (JD)
+   Microsoft (MSFT)
+   Micron Technology (MU)
+   Twitter (TWTR)
+   S&P 500 (^GSPC)

Daily Stock Quotes Sample:

![Screenshot](/png/stock_quotes.png)

## Beta Calculator

### Usage Example
Calculate the `Beta` of the selected stock eg. Citigroup (C).

```
import beta_calculator as bc

beta = bc.run("C")

print(beta)
```

### Output
Stock's Beta Coefficient and Beta Chart.

![Screenshot](/png/beta_out.png)

## Historical Volatility Calculator

### Usage Example
Calculate the `Annual Historical Volatility` for the selected stock eg. Micron (MU) and the S&P 500 Index for a specified period.

```
import historical_volatility_calculator as hvc

hv_vals = hvc.run("MU", 30)

print(hv_vals)
```

### Output
Tuple object, the first HV value for the stock, the second HV value for S&P500 index and HV Chart.

![Screenshot](/png/hv_out.png)

## Correlation Coefficient Calculator

### Usage Example
Calculate the `Correlation Coefficient` for the selected stocks eg. Micron (MU) and Citigroup (C).

```
import correlation_calculator as cc

corr = cc.run("MU", "C")

print(corr)
```

### Output
Stocks' Correlation Coefficient and Correlation Chart.

![Screenshot](/png/corr_out.png)

## LICENSE
MIT

## Contributions
Contributions to Statistical Tools are always welcome.  
If you have questions, suggestions or want to improve this repository, please create an [issue](https://github.com/Zsolt-Forray/statistical-tools/issues) or [pull requests](https://github.com/Zsolt-Forray/statistical-tools/pulls).  
This repo is maintained by Zsolt Forray (forray.zsolt@gmail.com).
