import unittest
from datetime import datetime, timedelta

from scipy.stats import gmean
from app.stock import Stock
from app.market import Market
from app.trade import Trade


class TestMarket(unittest.TestCase):
    def setUp(self):
        self.market = Market()
        self.market.add_stock(Stock("TEA", 0, 100, 100.0))
        self.market.add_stock(Stock("POP", 8, 100, 120.0))
        self.market.add_stock(Stock("ALE", 23, 60, 130.0))

    def test_update_multiple_stock_prices(self):
        updates = {"TEA": 110.0, "POP": 125.0}
        self.market.update_stock_prices(updates)
        self.assertEqual(self.market.stocks["TEA"].price, 110.0, "TEA stock price should be updated to 110.0")
        self.assertEqual(self.market.stocks["POP"].price, 125.0, "POP stock price should be updated to 125.0")
        self.assertEqual(self.market.stocks["ALE"].price, 130.0, "ALE stock price should remain unchanged at 130.0")

    def test_update_stock_price_positive(self):
        """Test updating a stock price with a positive value."""
        self.market.update_stock_price("TEA", 110.0)
        self.assertEqual(self.market.stocks["TEA"].price, 110.0, "Stock price should be updated to 110.0")

    def test_update_stock_price_to_zero(self):
        """Test updating a stock price to zero, which should raise an error."""
        with self.assertRaises(ValueError) as context:
            self.market.update_stock_price("TEA", 0)
        self.assertIn(
            "Stock price must be positive",
            str(context.exception),
            "Error message should indicate that stock price must be positive",
        )

    def test_update_stock_price_negative(self):
        """Test updating a stock price to a negative value, which should raise an error."""
        with self.assertRaises(ValueError) as context:
            self.market.update_stock_price("TEA", -100.0)
        self.assertIn(
            "Stock price must be positive",
            str(context.exception),
            "Error message should indicate that stock price must be positive",
        )

    def test_update_nonexistent_stock(self):
        """Test updating the price of a stock that doesn't exist in the market."""
        with self.assertRaises(KeyError) as context:
            self.market.update_stock_price("XXX", 200.0)
        self.assertIn(
            "No stock found with symbol: XXX", str(context.exception), "Error message should indicate no stock found"
        )

    def test_record_valid_trade(self):
        """Test recording a valid trade"""
        trade = Trade(1, self.market.stocks["TEA"], 150, "BUY", 101.0)
        self.market.record_trade(trade)
        self.assertEqual(len(self.market.trades), 1)
        self.assertEqual(trade.trade_id, 1)
        self.assertEqual(trade.stock.symbol, "TEA")
        self.assertEqual(trade.quantity, 150)
        self.assertEqual(trade.action, "BUY")
        self.assertEqual(self.market.trades[0].traded_price, 101.0)
        self.assertTrue(isinstance(trade.timestamp, datetime), "Timestamp should be a datetime object")

    def test_record_trade_nonexistent_stock(self):
        trade = Trade(2, Stock("XYZ", 0, 100, 100.0), 100, "SELL", 110.0)
        with self.assertRaises(ValueError):
            self.market.record_trade(trade)
        self.assertEqual(len(self.market.trades), 0, "Trade count should not increase")

    def test_record_trade_with_explicit_timestamp(self):
        """Test recording a trade with an explicit timestamp"""
        custom_time = datetime(2021, 5, 21, 14, 30)
        trade = Trade(3, self.market.stocks["POP"], 200, "SELL", 122.0, timestamp=custom_time)
        self.market.record_trade(trade)
        trade_recorded = self.market.trades[-1]
        self.assertEqual(trade_recorded.timestamp, custom_time, "Trade timestamp should match the provided timestamp")


class TestVWSP(unittest.TestCase):
    def setUp(self):
        """Set up a market with predefined stocks and trades"""
        self.market = Market()
        self.market.add_stock(Stock("TEA", 0, 100, 100.0))
        self.market.add_stock(Stock("POP", 8, 100, 120.0))

        ct = datetime.now()
        # Creating and adding trades with past timestamps
        trade1 = Trade(1, self.market.stocks["TEA"], 100, "BUY", 101.0, timestamp=ct - timedelta(minutes=30))
        trade2 = Trade(2, self.market.stocks["TEA"], 200, "SELL", 102.0, timestamp=ct - timedelta(minutes=29))
        trade3 = Trade(3, self.market.stocks["POP"], 150, "BUY", 119.0, timestamp=ct - timedelta(minutes=28))
        trade4 = Trade(3, self.market.stocks["POP"], 150, "BUY", 119.0, timestamp=ct - timedelta(minutes=5))
        self.market.record_trade(trade1)
        self.market.record_trade(trade2)
        self.market.record_trade(trade3)
        self.market.record_trade(trade4)

    def test_volume_weighted_stock_price_recent(self):
        """Test that the volume weighted stock price is correctly calculated for recent trades"""
        expected_vwsp_tea = ((101.0 * 100) + (102.0 * 200)) / (100 + 200)
        calculated_vwsp_tea = self.market.volume_weighted_stock_price("TEA", 60)
        self.assertAlmostEqual(
            calculated_vwsp_tea, expected_vwsp_tea, 2, "VWSP calculation should match expected for TEA"
        )

    def test_volume_weighted_stock_price_no_recent_trades(self):
        """Test VWSP calculation when there are no recent trades within the specified timeframe"""
        calculated_vwsp_tea = self.market.volume_weighted_stock_price("TEA", 15)
        self.assertEqual(calculated_vwsp_tea, 0, "VWSP should be 0 when there are no trades in the timeframe")

    def test_volume_weighted_stock_price_different_stock(self):
        """Test VWSP calculation for a different stock to ensure correct filtering of trades by stock symbol"""
        expected_vwsp_pop = ((119.0 * 150)) / (150)
        calculated_vwsp_pop = self.market.volume_weighted_stock_price("POP", 15)
        self.assertAlmostEqual(
            calculated_vwsp_pop, expected_vwsp_pop, 2, "VWSP calculation should match expected for POP"
        )


class TestGeometricMean(unittest.TestCase):
    def setUp(self):
        """Set up a market with predefined stocks"""
        self.market = Market()
        self.market.add_stock(Stock("TEA", 0, 100, 100.0))
        self.market.add_stock(Stock("POP", 8, 100, 120.0))
        self.market.add_stock(Stock("ALE", 23, 60, 130.0))

    def test_geometric_mean_multiple_prices(self):
        """Test that the geometric mean is correctly calculated for multiple stock prices"""
        expected_gmean = gmean([100.0, 120.0, 130.0])
        calculated_gmean = self.market.geometric_mean_of_prices()
        self.assertAlmostEqual(
            calculated_gmean, expected_gmean, places=2, msg="Geometric mean should match expected value"
        )

    def test_geometric_mean_no_stocks(self):
        """Test geometric mean calculation when no stocks are available"""
        self.market.stocks.clear()  # Removing all stocks
        calculated_gmean = self.market.geometric_mean_of_prices()
        self.assertEqual(calculated_gmean, 0, "Geometric mean should be 0 when no stocks are available")

    def test_geometric_mean_one_stock(self):
        """Test geometric mean calculation when only one stock is available"""
        # Keeping only one stock in the market
        self.market.stocks = {"TEA": self.market.stocks["TEA"]}
        calculated_gmean = self.market.geometric_mean_of_prices()
        self.assertAlmostEqual(
            calculated_gmean, 100.0, 7, "Geometric mean of one stock price should be the price itself"
        )

    def test_geometric_mean_zero_prices(self):
        """Test geometric mean calculation when all stock prices are zero"""
        # Setting all stock prices to zero
        for stock in self.market.stocks.values():
            stock.price = 0
        calculated_gmean = self.market.geometric_mean_of_prices()
        self.assertEqual(calculated_gmean, 0, "Geometric mean should be 0 when all prices are zero")


# This allows the test to be run from the command line
if __name__ == "__main__":
    unittest.main()
