import tkinter as tk
from tkinter import ttk
import json

try:
    from .CryptoHelper import *
    from  . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# WEBSOCKET
class Ticker(BaseUI.Widget):
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


if __name__ == "__main__":
    root = tk.Tk()
    ticker = Ticker(root, "btcusdt")
    ticker.pack()
    ticker.start()
    root.mainloop()