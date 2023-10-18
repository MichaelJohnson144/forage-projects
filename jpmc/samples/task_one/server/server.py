import csv
import http.server
import json
import operator
import os.path
import re
import threading
from datetime import timedelta, datetime
from random import normalvariate, random
from socketserver import ThreadingMixIn

import dateutil.parser

# Config:
# Simulation param:
MARKET_OPEN = datetime.today().replace(hour=0, minute=30, second=0)
TEST = "test.csv"


# Mock Data:
def bounded_random_walk(_min, _max, std):
    # Generates a bounded random walk:
    _range = _max - _min
    while True:
        _max += normalvariate(0, std)
        yield abs((_max % (_range * 2)) - _range) + _min


def market(t0=MARKET_OPEN):
    frequency = (12, 36, 50)
    market_price = (60.0, 150.0, 1)
    spread = (2.0, 6.0, 0.1)
    # Generates a random series of market conditions, (time, market_price, spread):
    for hours, market_price_x, spread in zip(
        bounded_random_walk(*frequency),
        bounded_random_walk(*market_price),
        bounded_random_walk(*spread),
    ):
        yield t0, market_price_x, spread
        t0 += timedelta(hours=abs(hours))


def orders(hist):
    # Generates a random set of limit orders (time, side, market_price, size) from a series of
    # market conditions:
    overlap = 4
    for t, market_price, spread in hist:
        stock = "ABC" if random() > 0.5 else "DEF"
        side, d = ("sell", 2) if random() > 0.5 else ("buy", -2)
        order = round(normalvariate(market_price + (spread / d), spread / overlap), 2)
        size = int(abs(normalvariate(0, 100)))
        yield t, stock, side, order, size


# Order Book:
def add_book(book, order, size, _age=10):
    # Add a new order and size to a book, and age the rest of the book:
    yield order, size, _age
    for o, s, age in book:
        if age > 0:
            yield o, s, age - 1


def clear_order(order, size, book, operation=operator.ge, _notional=0):
    """Try to clear a sized order against a book, returning a tuple of `(notional, new_book)` if
    successful, and None if not. `_Notional` is a recursive accumulator and should not be
    provided by the caller:
    """
    (top_order, top_size, age), tail = book[0], book[1:]
    if operation(order, top_order):
        _notional += min(size, top_size) * top_order
        size_difference = top_size - size
        if size_difference > 0:
            return _notional, list(add_book(tail, top_order, size_difference, age))
        elif len(tail) > 0:
            return clear_order(order, -size_difference, tail, operation, _notional)


def clear_book(buy=None, sell=None):
    # Clears all crossed orders from a buy and sell book, returning the new books uncrossed:
    while buy and sell:
        order, size, _ = buy[0]
        new_book = clear_order(order, size, sell)
        if new_book:
            sell = new_book[1]
            buy = buy[1:]
        else:
            break
    return buy, sell


def order_book(_orders, book, stock_name):
    """Generates a series of order books from a series of orders. Order books are mutable lists,
    and mutating them during generation will affect the next turn!"""
    for t, stock, side, order, size in _orders:
        if stock_name == stock:
            new = add_book(book.get(side, []), order, size)
            book[side] = sorted(new, reverse=side == "buy", key=lambda x: x[0])
        bids, asks = clear_book(**book)
        yield t, bids, asks


def generate_csv():
    # Generate a CSV of order history:
    simulation_length = timedelta(days=365 * 5)
    with open(TEST, "w") as f:
        writer = csv.writer(f)
        for t, stock, side, order, size in orders(market()):
            if t > MARKET_OPEN + simulation_length:
                break
            writer.writerow([t, stock, side, order, size])


def read_csv():
    # Read a CSV or order history into a list:
    with open(TEST, "rt") as f:
        for time, stock, side, order, size in csv.reader(f):
            yield dateutil.parser.parse(time), stock, side, float(order), int(size)


# Server:
class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    # Boilerplate class for a multithreading HTTP Server, with working shutdown:
    allow_reuse_address = True

    def shutdown(self):
        # Override MRO to shut down properly.
        self.socket.close()
        http.server.HTTPServer.shutdown(self)


def route(path):
    """Decorator for a simple bottle-like web framework. Routes a path to the decorated method,
    with the rest of the path as an argument:"""

    def _route(f):
        setattr(f, "__route__", path)
        return f

    return _route


def read_params(path):
    # Read query parameters into a dictionary if they are parseable, otherwise returns None:
    query = path.split("?")
    if len(query) > 1:
        query = query[1].split("&")
        return dict(map(lambda x: x.split("="), query))


def get(req_handler, routes):
    # Map a request to the appropriate route of a routes instance:
    for name, handler in routes.__class__.__dict__.items():
        if hasattr(handler, "__route__"):
            if re.search(handler.__route__, req_handler.path) is not None:
                req_handler.send_response(200)
                req_handler.send_header("Content-Type", "application/json")
                req_handler.send_header("Access-Control-Allow-Origin", "*")
                req_handler.end_headers()
                params = read_params(req_handler.path)
                data = json.dumps(handler(routes, params)) + "\n"
                req_handler.wfile.write(bytes(data, encoding="utf-8"))
                return


def run(routes, host="0.0.0.0", port=8080):
    # Runs a class as a server whose methods have been decorated with `@route`:
    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            # pass
            pass

        def do_GET(self):
            get(self, routes)

    server = ThreadedHTTPServer((host, port), RequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print("HTTP server started on port 8080")
    try:
        while True:
            from time import sleep

            sleep(1)
    except KeyboardInterrupt:
        server.shutdown()


# App:
operations = {
    "buy": operator.le,
    "sell": operator.ge,
}


class App(object):
    # The trading game server application:
    def __init__(self):
        self._book_1 = dict()
        self._book_2 = dict()
        self._data_1 = order_book(read_csv(), self._book_1, "ABC")
        self._data_2 = order_book(read_csv(), self._book_2, "DEF")
        self.realtime = True
        self._rt_start = datetime.now()
        self._sim_start, _, _ = next(self._data_1)
        self.read_10_first_lines()

    @property
    def _current_book_1(self):
        for t, bids, asks in self._data_1:
            if self.realtime:
                while t > self._sim_start + (datetime.now() - self._rt_start):
                    yield t, bids, asks
            else:
                yield t, bids, asks

    @property
    def _current_book_2(self):
        for t, bids, asks in self._data_2:
            if self.realtime:
                while t > self._sim_start + (datetime.now() - self._rt_start):
                    yield t, bids, asks
            else:
                yield t, bids, asks

    def read_10_first_lines(self):
        for _ in iter(range(10)):
            next(self._data_1)
            next(self._data_2)

    @route("/query")
    def handle_query(self, x):
        try:
            t1, bids_a, asks_a = next(self._current_book_1)
            t2, bids_b, asks_b = next(self._current_book_2)
        except (StopIteration, ValueError) as e:
            print("Error getting stocks:", str(e))
            print("Reinitializing app...")
            self.__init__()
            t1, bids_a, asks_a = next(self._current_book_1)
            t2, bids_b, asks_b = next(self._current_book_2)

        t = t1 if t1 > t2 else t2
        print("Query received @ t%s" % t)
        return [
            {
                "id": x and x.get("id", None),
                "stock": "ABC",
                "timestamp": str(t),
                "top_bid": bids_a
                and {
                    "market_price": bids_a[0][0],
                    "size": bids_a[0][1],
                },
                "top_ask": asks_a
                and {
                    "market_price": asks_a[0][0],
                    "size": asks_a[0][1],
                },
            },
            {
                "id": x and x.get("id", None),
                "stock": "DEF",
                "timestamp": str(t),
                "top_bid": bids_b
                and {
                    "market_price": bids_b[0][0],
                    "size": bids_b[0][1],
                },
                "top_ask": asks_b and {
                    "market_price": asks_b[0][0],
                    "size": asks_b[0][1],
                },
            },
        ]


if __name__ == "__main__":
    if not os.path.isfile(TEST):
        print("No data found, generating...")
        generate_csv()
    run(App())
