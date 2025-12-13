import websocket
import json
import threading
import requests


class WebsocketHelper(threading.Thread):
    '''
    Class for handling websocket connections.
    '''

    def __init__(self, url=None, on_message=None, on_error=None, on_close=None, on_open=None):
        super().__init__(daemon=True)
        self.url = url
        self.last_message = None
        self.active = False

        if self.url != None:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
        else:
            raise ValueError(
                "Object has no URL! Assign URL to object before running.")

    def run(self):
        self.active = True
        self.ws.run_forever()

    def close(self):
        # Ensure the run_forever loop breaks cleanly
        try:
            self.ws.keep_running = False
            self.ws.close()
            self.active = False
        except Exception as exc:
            print(f"Close error: {exc}")

        self.active = False
        print("WebSocket close requested.")


class CryptoWS(WebsocketHelper):
    '''
    Class for handling Binance's Websocket
    '''

    def __init__(self, base="wss://stream.binance.com:9443/ws/", stream=None, 
                on_message=None, on_error=lambda ws, err: print(f"WS error: {err}"),
                on_close=lambda ws, s, m: print(f"WS closed"),
                on_open=lambda ws: print(f"WS connected")):
        if stream != None:
            super().__init__(url=base+stream, on_message=on_message,
                             on_error=on_error, on_close=on_close, on_open=on_open)
        else:
            assert ("WEBSOCKET HAS NOT PROVIDED STREAM!")


class RESTHelper:
    '''
    CLass for handling REST API.
    '''

    def __init__(self, base_url=None):
        self.base_url = base_url
        if self.base_url is None:
            raise ValueError(
                "Object has no base URL! Assign base URL to object before running.")

    def get(self, goal, params):
        url = self.base_url + goal
        response = requests.get(url, params=params)
        return response.json()


class CryptoREST(RESTHelper):
    '''
    CLass for Binance's REST API.
    '''

    def __init__(self, base_url="https://api.binance.com"):
        super().__init__(base_url=base_url)

    def price(self, symbol):
        return self.get("/api/v3/ticker/price", {"symbol": symbol})

    def stat_24(self, symbol):  # Volume 24
        return self.get("/api/v3/ticker/24hr", {"symbol": symbol})

    def book_depth(self, symbol, limit=10):
        return self.get("/api/v3/depth", {"symbol": symbol, "limit": limit})

    def trades(self, symbol, limit=5):
        return self.get("/api/v3/trades", {"symbol": symbol, "limit": limit})

    def kline(self, symbol, interval="1h", limit=24):
        return self.get("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})


if __name__ == "__main__":
    a = 1
    n = CryptoREST()
    print(n.price("BTCUSDT"))

    # Fix: capture c1 in the lambda and set attribute on it, not ws
    c1 = CryptoWS(stream="btcusdt@trade")
    c1.on_message = lambda ws, msg: setattr(c1, "last_message", msg)

    # Or better: define a proper callback method
    def handle_message(ws, msg):
        c1.last_message = msg

    c1 = CryptoWS(stream="btcusdt@trade", on_message=handle_message)
    c1.start()

    past = None
    while True:
        if c1.last_message is not None and c1.last_message != past:
            past = c1.last_message
            print(c1.last_message)
            a += 1
        if a > 10:
            c1.close()
            print("Finished")
            break
