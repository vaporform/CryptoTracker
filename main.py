import tkinter as tk
from tkinter import ttk

from Components.Ticker import Ticker
from Components.Book import Book
from Components.PriceHistory import PriceHistory
from Components.TradeHistory import TradeHistory
from Components.VolumeHistory import VolumeHistory
from Components.KlineHistory import KlineHistory


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("1280x720")

        # --- Main Container ---
        mainframe = ttk.Frame(root, padding=10)
        mainframe.pack(fill=tk.BOTH, expand=True)

        # --- Grid Configuration ---
        # Col 0 (Left) & Col 2 (Right): Fixed width (weight=0)
        # Col 1 (Middle): Takes all extra horizontal space (weight=1)
        mainframe.columnconfigure(0, weight=0)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=0)

        # Row 0: Tickers (Fixed height, weight=0)
        # Row 1: Trade History (Takes remaining vertical space, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)

        self.btc_ticker = Ticker(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.btc_ticker.grid(row=0, column=0, sticky="nsew")

        self.Trader = TradeHistory(
            mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Trader.grid(row=1, column=0, sticky="nsew",
                         pady=(10, 0), padx=(0, 5))

        self.Kline = KlineHistory(
            mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Kline.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5)

        self.Book = Book(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Book.grid(row=0, column=2, rowspan=2, sticky="nsew")

        self.Book.start()
        self.Trader.start()
        self.Kline.start()
        self.btc_ticker.start()

    def on_closing(self):
        '''Clean up for those websockets.'''
        self.Trader.stop()
        self.btc_ticker.stop()
        self.Book.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
