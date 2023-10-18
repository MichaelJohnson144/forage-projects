import json
from unittest.mock import patch

from jpmc.samples.task_one.client.client import Client


class TestClient:
    def test_get_data_point(self):
        # Mock data for testing
        quote_data = {
            "stock": "ABC",
            "top_bid": {"market_price": "10.0"},
            "top_ask": {"market_price": "12.0"},
        }

        # Test get_data_point function
        stock, bid_price, ask_price, market_price = Client().get_data_point(quote_data)
        assert stock == "ABC"
        assert bid_price == 10.0
        assert ask_price == 12.0
        assert market_price == 11.0

    def test_get_ratio(self):
        client = Client()
        # Test get_ratio function
        assert client.get_ratio(10.0, 5.0) == 2.0
        assert client.get_ratio(15.0, 3.0) == 5.0
        assert client.get_ratio(8.0, 8.0) == 1.0

    # Patch `urllib.request.urlopen` to return mock data:
    @patch("urllib.request.urlopen")
    def test_main(self, mock_urlopen):
        client = Client()
        # Mock the response from `urllib.request.urlopen`:
        mock_urlopen.return_value.read.return_value = (
            '[{"stock": "ABC", "top_bid": {"market_price": "10.0"}, "top_ask":'
            ' {"market_price": "12.0"}}]'
        )

        # Perform the test
        with patch("builtins.print") as mock_print:
            # Call the functions directly instead of using `exec(open(`client_test.py`).read())`:
            quotes = json.loads(mock_urlopen.return_value.read.return_value)
            market_prices = {}
            for quote in quotes:
                stock, bid_price, ask_price, price = client.get_data_point(quote)
                market_prices[stock] = price
                print(
                    "Quoted %s at (Bid: $%s, Ask: $%s, Market Price: $%s)"
                    % (stock, bid_price, ask_price, price)
                )
            if "ABC" in market_prices and "DEF" in market_prices:
                ratio = client.get_ratio(market_prices["ABC"], market_prices["DEF"])
                print("Ratio %s" % ratio)
            else:
                print("Cannot calculate ratio: Missing stock data")

            # Assert the print calls:
            assert mock_print.call_count == 2
            assert (
                mock_print.call_args_list[0][0][0]
                == "Quoted ABC at (Bid: $10.0, Ask: $12.0, Market Price: $11.0)"
            )
            assert (
                mock_print.call_args_list[1][0][0]
                == "Cannot calculate ratio: Missing stock data"
            )
