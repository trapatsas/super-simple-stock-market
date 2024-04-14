import logging
from datetime import datetime, timedelta

from scipy.stats import gmean


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Market:
    """Market class to represent the stock market."""

    def __init__(self):
        self.stocks = {}
        self.trades = []

    def add_stock(self, stock):
        self.stocks[stock.symbol] = stock

    def record_trade(self, trade):
        """Requirement 3: Build a function to record a trade.
        Records a trade in the market.

        Args:
            trade (Trade): The trade to record.

        Raises:
            ValueError: If the trade is attempted on a non-listed stock.
        """
        if trade.stock.symbol in self.stocks:
            self.trades.append(trade)
            logging.info("Recorded trade: %s", trade)
        else:
            logging.error("Trade attempted on non-listed stock.")
            raise ValueError("Trade attempted on non-listed stock.")

    def update_stock_price(self, symbol, price):
        if symbol in self.stocks:
            if price <= 0:
                logging.error("Stock price must be positive.")
                raise ValueError("Stock price must be positive.")
            self.stocks[symbol].price = price
        else:
            logging.error("No stock found with symbol: %s", symbol)
            raise KeyError(f"No stock found with symbol: {symbol}")

    def update_stock_prices(self, updates):
        # Requirement 2: Update multiple stock prices at once.
        for symbol, price in updates.items():
            if symbol in self.stocks:
                self.update_stock_price(symbol, price)

    def volume_weighted_stock_price(self, stock_symbol, minutes=15):
        # Requirement 4: Returns the Volume Weighted Stock Price on the trades in the past 15 minutes, for a given stock.
        now = datetime.now()
        relevant_trades = [
            t
            for t in self.trades
            if t.stock.symbol == stock_symbol and (now - t.timestamp) <= timedelta(minutes=minutes)
        ]
        total_quantity = sum(t.quantity for t in relevant_trades)
        total_traded = sum(t.traded_price * t.quantity for t in relevant_trades)
        return total_traded / total_quantity if total_quantity > 0 else 0

    def geometric_mean_of_prices(self):
        # Requirement 5: Computes the Geometric Mean of prices for all stocks.
        prices = [stock.price for stock in self.stocks.values()]
        return gmean(prices) if prices else 0
