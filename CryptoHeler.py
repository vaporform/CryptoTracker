import websocket
import json
import threading
import requests
import time

class WebsocketHelper(threading.Thread):
    '''
    Class for handling websocket connections.
    '''
    def __init__(self,url=None):
        super().__init__(daemon=True)
        self.url = url
        self.last_message = None
        
        if self.url != None:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )
        else:
            raise ValueError("Object has no URL! Assign URL to object before running.")
    
    def on_message(self,ws, message):
        data = json.loads(message)
        self.last_message = data

    def on_error(self,ws, error):
        print(f"Error: {error}")

    def on_close(self,ws, close_status, close_msg):
        print("Connection closed")

    def on_open(self,ws):
        print("Connected to URL.")

    def run(self):
        self.ws.run_forever()

    def close(self):
        # Ensure the run_forever loop breaks cleanly
        try:
            self.ws.keep_running = False
            self.ws.close()
        except Exception as exc:
            print(f"Close error: {exc}")

        print("WebSocket close requested.")

        # Avoid deadlock if close is called from within the same thread
        if threading.current_thread() is self:
            return True

        self.join(timeout=5)
        if self.is_alive():
            print("Warning: websocket thread did not exit within timeout.")
        return True

class CryptoWS(WebsocketHelper):
    def __init__(self,base="wss://stream.binance.com:9443/ws/",stream=None):
        if stream != None:
            super().__init__(url=base+stream)
        else:
            assert("WEBSOCKET HAS NOT PROVIDED STREAM!")

class RESTHelper:
    '''
    CLass for handling REST API.
    '''
    def __init__(self,base_url=None):
        self.base_url = base_url
        if self.base_url is None:
            raise ValueError("Object has no base URL! Assign base URL to object before running.")
        
    def get(self,goal,params):
        url = self.base_url + goal
        response = requests.get(url, params=params)
        return response.json()
    
class CryptoREST(RESTHelper):
    '''
    CLass for Binance's REST API.
    '''
    def __init__(self,base_url="https://api.binance.com"):
        super().__init__(base_url=base_url)

    def price(self,symbol):
        return self.get("/api/v3/ticker/price",{"symbol":symbol})

    def stat_24(self,symbol):
        return self.get("/api/v3/ticker/24hr",{"symbol":symbol})

    def book_depth(self,symbol,limit=10):
        return self.get("/api/v3/depth",{"symbol":symbol,"limit":limit})

    def trades(self,symbol,limit=5):
        return self.get("/api/v3/trades",{"symbol":symbol,"limit":limit})

    def kline(self,symbol,interval="1h",limit=24):
        return self.get("/api/v3/klines",{"symbol":symbol,"interval":interval,"limit":limit})

if __name__ == "__main__":
    a = 1
    n = CryptoREST()
    print(n.price("BTCUSDT"))
    '''
    c1 = CryptoWebSocket(url="wss://stream.binance.com:9443/ws/btcusdt@trade")
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
    '''