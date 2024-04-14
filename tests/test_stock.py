import unittest

from app.stock import Stock, PreferredStock


class TestStock(unittest.TestCase):
    def test_dividend_yield_common(self):
        # Test common stock dividend yield calculation
        stock = Stock("TEA", 8, 100, 40)
        self.assertEqual(stock.calculate_dividend_yield(), 0.2)

    def test_dividend_yield_preferred(self):
        # Test preferred stock dividend yield calculation
        stock = PreferredStock("GIN", 8, 0.02, 100, 50)
        self.assertAlmostEqual(stock.calculate_dividend_yield(), 0.04, places=2)

    def test_dividend_yield_zero_price(self):
        # Test to ensure behavior when price is zero (to avoid division by zero errors)
        stock = Stock("ALE", 23, 60, 0)
        with self.assertRaises(ZeroDivisionError):
            stock.calculate_dividend_yield()

    def test_dividend_yield_negative_price(self):
        # Test for negative stock price scenarios
        stock = Stock("POP", 10, 100, -50)
        self.assertEqual(stock.calculate_dividend_yield(), -0.2)


# This allows the test to be run from the command line
if __name__ == "__main__":
    unittest.main()
