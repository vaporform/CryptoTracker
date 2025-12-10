import tkinter as tk
from tkinter import ttk
import json

import matplotlib
from CryptoHelper import *
import BaseGUI

class Ticker(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.is_active = False
        self.symbol = symbol
        self.websocket = CryptoWS(stream=f"{self.symbol}@ticker"
                                ,on_message=self.on_message
                                ,on_error=lambda ws, err: print(f"{self.symbol} error: {err}")
                                ,on_close=lambda ws, s, m: print(f"{self.symbol} closed")
                                ,on_open=lambda ws: print(f"{self.symbol} connected")
                                )
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)
        # Price
        self.price_label = tk.Label(target, text="--,---", 
                                    font=("Arial", 40, "bold"))
        self.price_label.pack(pady=10)
        
        # Change
        self.change_label = ttk.Label(target, text="--", 
                                      font=("Arial", 12))
        self.change_label.pack()
    
    def on_message(self, ws, message):
        """Handle price updates."""
        if not self.is_active:
            return
        
        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])
        
        # Schedule GUI update on main thread
        self.parent.after(0, self.update_display, price, change, percent)
    
    def update_display(self, price, change, percent):
        """Update the ticker display."""
        if not self.is_active:
            return
        
        color = "green" if change >= 0 else "red"
        self.price_label.config(text=f"{price:,.2f}", fg=color)
        
        sign = "+" if change >= 0 else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            foreground=color
        )
    
    def start(self):
        """Start the ticker updates."""
        if self.is_active:
            return
        self.is_active = True
        self.websocket.start()
    
    def stop(self):
        """Stop the ticker updates."""
        if not self.is_active:
            return
        self.is_active = False
        self.websocket.close()

class Book(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_book(self):
        """Fetch order book."""
        book = CryptoREST().book_depth(self.symbol, limit=10)
        print(book)
        return book

class VolumeHistory(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_volume_history(self):
        """Fetch volume history."""
        stats = CryptoREST().stat_24(self.symbol)
        print(stats)
        return stats

class TradeHistory(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_trade_history(self):
        """Fetch trade history."""
        trades = CryptoREST().trades(self.symbol, limit=5)
        print(trades)
        return trades

class PriceHistory(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_price_history(self):
        """Fetch price history."""
        price = CryptoREST().price(self.symbol)
        print(price)
        return price

class KlineHistory(BaseGUI.Widget):
    def __init__(self, parent,symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
            font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_kline_history(self):
        """Fetch kline history."""
        klines = CryptoREST().kline(self.symbol, interval="1h", limit=24)
        print(klines)
        return klines

if __name__ == "__main__":
    root = tk.Tk()
    ticker = Ticker(root, "btcusdt")
    ticker.pack()
    ticker.start()
    root.mainloop()