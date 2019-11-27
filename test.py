#!/usr/bin/python3


"""
Test for the statistical tools
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '27/11/2019'
__status__  = 'Development'


import unittest
import beta_calculator as bc
import correlation_calculator as cc
import historical_volatility_calculator as hvc


class TestBeta(unittest.TestCase):
    def test_beta(self):
        beta = bc.Beta("MU")
        self.assertEqual(beta.run_app(), 1.82)

    def test_invalid_ticker(self):
        beta = bc.Beta("KO")
        self.assertEqual(beta.run_app(), None)


class TestCorrelation(unittest.TestCase):
    def test_correlation(self):
        corr = cc.Correlation("MU", "C")
        self.assertEqual(corr.run_app(), 0.34)

    def test_invalid_ticker(self):
        corr = cc.Correlation("F", "KO")
        self.assertEqual(corr.run_app(), None)


class TestHVol(unittest.TestCase):
    def test_hv(self):
        hv = hvc.HVol("MU", 30)
        self.assertEqual(hv.run_app(), ("58.52%", "26.71%"))

    def test_invalid_ticker(self):
        hv = hvc.HVol("F", 40)
        self.assertEqual(hv.run_app(), None)

    def test_float_period(self):
        hv = hvc.HVol("AMAT", 40.45)
        self.assertEqual(hv.run_app(), None)

    def test_period_below(self):
        hv = hvc.HVol("AMAT", 1)
        self.assertEqual(hv.run_app(), None)

    def test_period_above(self):
        hv = hvc.HVol("AMAT", 300)
        self.assertEqual(hv.run_app(), None)


if __name__ == "__main__":
    unittest.main()
