from datetime import datetime


class Trade:
    """Trade class to represent a trade in the stock market."""

    def __init__(self, trade_id, stock, quantity, action, traded_price, timestamp=None):
        self.trade_id = trade_id
        self.stock = stock
        self.quantity = quantity
        self.action = action
        self.traded_price = traded_price
        self.timestamp = timestamp if timestamp else datetime.now()

    def __repr__(self):
        return f"Trade({self.trade_id}, {self.stock}, {self.quantity}, {self.action}, {self.traded_price}, {self.timestamp})"
