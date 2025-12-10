import tkinter as tk
from tkinter import ttk

from CryptoGUI import *

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("800x300")
        
        # Create ticker panel
        ticker_frame = ttk.Frame(root, padding=20)
        ticker_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create BTC ticker
        self.btc_ticker = Ticker(ticker_frame, "btcusdt")
        self.btc_ticker.pack()

        # Create AAA ticker
        self.aaa = Ticker(ticker_frame, "metusdt")
        self.aaa.pack()
        
        self.btc_ticker.start()
        self.aaa.start()
    
    def on_closing(self):
        """Clean up when closing."""
        self.aaa.stop()
        self.btc_ticker.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()