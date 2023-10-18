import json
import random
import urllib.request


class Client:
    def get_data_point(self, quote_data):
        # Produce all the needed values to generate a datapoint:
        _stock = quote_data["stock"]
        _bid_price = float(quote_data["top_bid"]["market_price"])
        _ask_price = float(quote_data["top_ask"]["market_price"])
        _market_price = (_bid_price + _ask_price) / 2
        return self and _stock, _bid_price, _ask_price, _market_price

    def get_ratio(self, market_price_a, market_price_b):
        # Get the ratio of `market_price_a` and `market_price_b`:
        return self and market_price_a / market_price_b


if __name__ == "__main__":
    # 500 server request:
    N = 500

    # Server API URLs:
    QUERY = "http://localhost:8080/query?id={}"

    # Create an instance of the Client class:
    client = Client()

    # Query the price once every N second:
    for _ in range(N):
        quotes = json.loads(
            urllib.request.urlopen(QUERY.format(random.random())).read()
        )
        market_prices = {}
        for quote in quotes:
            stock, bid_price, ask_price, market_price = client.get_data_point(quote)
            market_prices[stock] = market_price
            print(
                "Quoted %s at (Bid: $%s, Ask: $%s, Market Price: $%s)"
                % (stock, bid_price, ask_price, market_price)
            )
        print("Ratio %s" % client.get_ratio(market_prices["ABC"], market_prices["DEF"]))
