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
        '''
        Run the websocket configured from initialization.
        '''

        self.active = True
        self.ws.run_forever()

    def close(self):
        '''
        Close the websocket
        '''
        print("Websocket close requested.")
        try:
            self.ws.keep_running = False
            self.ws.close()
            self.active = False
        except Exception as exc:
            print(f"Close error: {exc}")

        self.active = False
        print("Websocket closed.")


class CryptoWS(WebsocketHelper):
    '''
    Class for handling Binance's Websocket.
    '''

    # Note: The websocket comes with dummy functions. It is crucial to replace
    # the functions with your intended methods.

    def __init__(self, base="wss://stream.binance.com:9443/ws/", stream=None, 
                on_message=None, on_error=lambda ws, err: print(f"WS error: {err}"),
                on_close=lambda ws, s, m: print(f"WS closed"),
                on_open=lambda ws: print(f"WS connected")):

        if stream != None:
            super().__init__(url=base+stream, on_message=on_message,
                             on_error=on_error, on_close=on_close, on_open=on_open)
        else:
            raise ValueError("Websocket has not provided stream!")


class RESTHelper:
    '''
    Class for handling REST API.
    '''

    def __init__(self, base_url=None):
        self.base_url = base_url
        if self.base_url is None:
            raise ValueError("Object has no base URL! Assign base URL to object before running.")

    def get(self, goal, params):
        '''
        Simply get response from REST.
        '''

        url = self.base_url + goal
        response = requests.get(url, params=params)
        return response.json()


class CryptoREST(RESTHelper):
    '''
    Class for Binance's REST API.
    '''

    def __init__(self, base_url="https://api.binance.com"):
        super().__init__(base_url=base_url)

    def price(self, symbol):
        '''
        Get the price of the symbol.
        '''

        return self.get("/api/v3/ticker/price", {"symbol": symbol})

    def stat_24(self, symbol):  # Volume 24
        '''
        Get the 24 hour stats of the symbol.
        '''

        return self.get("/api/v3/ticker/24hr", {"symbol": symbol})

    def book_depth(self, symbol, limit=10):
        '''
        Get the book of the symbol.
        '''
        
        return self.get("/api/v3/depth", {"symbol": symbol, "limit": limit})

    def trades(self, symbol, limit=5):
        '''
        Get the trades of the symbol.
        '''
        
        return self.get("/api/v3/trades", {"symbol": symbol, "limit": limit})

    def kline(self, symbol, interval="1h", limit=24):
        '''
        Get the necessary kline info of the symbol.
        '''
        
        return self.get("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})


if __name__ == "__main__":
    '''
    Testing Websockets and REST Methods.
    '''

    a = 1
    n = CryptoREST()
    print(n.price("BTCUSDT"))

    last_msg = ""
    past = ""

    def handle_message(ws, msg):
        global a
        last_msg = msg
        print(msg)
        a += 1

    c1 = CryptoWS(stream="btcusdt@trade", on_message=handle_message)
    c1.start()

    while True:
        if a > 10:
            c1.close()
            print("Finished")
            break
    
