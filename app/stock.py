import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Stock:
    """
    A class to represent a stock.
    """

    def __init__(self, symbol, last_dividend, par_value, price):
        self.symbol = symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.price = price

    def calculate_dividend_yield(self):
        """Requirement 1a: Provide a function to return the Dividend Yield for any given stock.
        Calculate the dividend yield of the stock.

        Returns:
            float: The dividend yield of the stock.
        """
        return self.last_dividend / self.price

    def __repr__(self):
        return f"Stock({self.symbol}, {self.last_dividend}, {self.par_value}, {self.price})"


class PreferredStock(Stock):
    """A class to represent a preferred stock. Inherits from Stock.

    Args:
        Stock (class): The parent class.
        fixed_dividend_ratio (float): The fixed dividend ratio of the preferred stock.
    """

    def __init__(self, symbol, last_dividend, fixed_dividend_ratio, par_value, price):
        super().__init__(symbol, last_dividend, par_value, price)
        self.fixed_dividend_ratio = fixed_dividend_ratio

    def calculate_dividend_yield(self):
        """Requirement 1b: Provide a function to return the Dividend Yield for any given stock.
        Calculate the dividend yield of the preferred stock.

        Returns:
            float: The dividend yield of the preferred stock.
        """
        return (self.fixed_dividend_ratio * self.par_value) / self.price

    def __repr__(self):
        return f"PreferredStock({self.symbol}, {self.last_dividend}, {self.fixed_dividend_ratio}, {self.par_value}, {self.price})"
