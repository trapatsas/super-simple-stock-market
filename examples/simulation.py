from random import randint, choice

from app.market import Market
from app.stock import Stock, PreferredStock
from app.trade import Trade


def simulate_stock_activity(market):
    stock_symbols = list(market.stocks.keys())
    for _ in range(10):  # Simulate 10 trading actions
        stock_symbol = choice(stock_symbols)
        stock = market.stocks[stock_symbol]
        action = choice(["BUY", "SELL"])
        quantity = randint(1, 100)  # Random quantity between 1 and 100
        traded_price = stock.price * (1 + randint(-5, 5) / 100.0)  # Simulate price fluctuation
        trade = Trade(randint(1000, 9999), stock, quantity, action, traded_price)
        market.record_trade(trade)
        # For this simulation, we will also update the stock price to reflect the latest traded price
        stock.price = traded_price


def main():
    market = Market()
    # Adding some stocks to the market
    market.add_stock(Stock("TEA", 0, 100, 34.42))
    market.add_stock(PreferredStock("POP", 10, 0.035, 100, 47.48))
    market.add_stock(Stock("ALE", 23, 60, 24.43))
    market.add_stock(PreferredStock("GIN", 8, 0.02, 100, 15.45))
    market.add_stock(Stock("JOE", 13, 250, 33.52))

    # Let's first calculate the dividend yield for each stock, as per Requirement 1
    for symbol, stock in market.stocks.items():
        print(f"Dividend Yield for {symbol}: {stock.calculate_dividend_yield():.2f}")

    # Simulate trading activity
    simulate_stock_activity(market)

    # Display all trades
    for trade in market.trades:
        print(trade)

    # Calculate and print the geometric mean of stock prices
    geom_mean = market.geometric_mean_of_prices()
    print(f"Geometric Mean of Prices: {geom_mean:.2f}")

    # Calculate and print the VWSP for one of the stocks
    for symbol in market.stocks:
        vwsp = market.volume_weighted_stock_price(symbol)
        print(f"Volume Weighted Stock Price for {symbol}: {vwsp:.2f}")


if __name__ == "__main__":
    main()
