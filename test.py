#!/usr/bin/python3

import unittest
import beta_calculator as bc
import correlation_calculator as cc
import historical_volatility_calculator as hvc


class TestBeta(unittest.TestCase):
    def test_beta(self):
        self.assertEqual(bc.run("MU"), 1.82)

    def test_invalid_ticker(self):
        self.assertEqual(bc.run("KO"), None)


class TestCorrelation(unittest.TestCase):
    def test_correlation(self):
        self.assertEqual(cc.run("MU", "C"), 0.34)

    def test_invalid_ticker(self):
        self.assertEqual(cc.run("F", "KO"), None)


class TestHistoricalVolatility(unittest.TestCase):
    def test_hv(self):
        self.assertEqual(hvc.run("MU", 30), ("58.52%", "26.71%"))

    def test_invalid_ticker(self):
        self.assertEqual(hvc.run("F", 40), None)

    def test_float_period(self):
        self.assertEqual(hvc.run("AMAT", 40.45), None)

    def test_period_below(self):
        self.assertEqual(hvc.run("AMAT", 1), None)

    def test_period_above(self):
        self.assertEqual(hvc.run("AMAT", 300), None)


if __name__ == "__main__":
    unittest.main()
