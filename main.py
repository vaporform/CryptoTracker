import websocket
import json
import time
def on_message(ws, message):
    data = json.loads(message)
    print(f"BTC Price: ${data['c']}")  # 'c' is current price

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connected to Binance")

# WebSocket URL for BTC/USDT ticker
ws_url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

ws = websocket.WebSocketApp(
    ws_url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open
)

ws.run_forever()
past = ws.on_message
while True:
    if past != str(ws.on_message):
        past = str(ws.on_message)
        print(ws.on_message)
