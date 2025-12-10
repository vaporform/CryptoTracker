import websocket
import json
import threading    

class CryptoWebSocket(threading.Thread):
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

if __name__ == "__main__":
    c1 = CryptoWebSocket(url="wss://stream.binance.com:9443/ws/btcusdt@trade")
    c1.start()

    past = None
    while True:
        if c1.last_message is not None and c1.last_message != past:
            past = c1.last_message
            print(c1.last_message)