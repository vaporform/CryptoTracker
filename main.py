import tkinter as tk
from tkinter import ttk

from Components.Ticker import Ticker
from Components.Book import Book
from Components.PriceHistory import PriceHistory
from Components.TradeHistory import TradeHistory
from Components.VolumeHistory import VolumeHistory
from Components.KlineHistory import KlineHistory
from Components.CryptoHelper import CryptoWS

class Application:
    def __init__(self, root):
        self.cryptos = [
            'btcusdt',
            'ethusdt',
            'solusdt',
            'xrpusdt',
            'dogeusdt'
        ]
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

        # Row 0: Options (Fixed height)
        # Row 1: Ticker (Fixed height)
        # Row 2: Trade History (Takes remaining vertical space)
        mainframe.rowconfigure(0, weight=0)
        mainframe.rowconfigure(1, weight=0)
        mainframe.rowconfigure(2, weight=1)

    
        # WIDGET STUFF DOWN HERE!
        self.selected_crypto = tk.StringVar(self.root)
        self.selected_crypto.set(self.cryptos[0]) # default value

        self.Options = ttk.OptionMenu(mainframe, self.selected_crypto, self.cryptos[0], *self.cryptos)
        self.Options.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=(0, 5))
        
        self.Ticker = Ticker(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Ticker.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        self.Trader = TradeHistory(
            mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Trader.grid(row=2, column=0, sticky="nsew",
                         pady=(5, 0), padx=(0, 5))

        self.Kline = KlineHistory(
            mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Kline.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=5)

        self.Book = Book(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Book.grid(row=0, column=2, rowspan=3, sticky="nsew")
        
        self.selected_crypto.trace_add("write", self.on_crypto_select)
        self.Book.start()
        self.Trader.start()
        self.Kline.start()
        self.Ticker.start()

    def on_crypto_select(self, *args):
        '''Callback for when a new crypto is selected from the dropdown.'''
        new_symbol = self.selected_crypto.get()
        new_title = new_symbol.replace('usdt', '').upper()
        new_sub = "USDT"

        self.Ticker.stop()
        self.Ticker.symbol = new_symbol
        self.Ticker.a.config(text=new_title)
        self.Ticker.b.config(text=new_sub)
        self.Ticker.websocket = CryptoWS(
            stream=f"{new_symbol}@ticker", on_message=self.Ticker.on_message)
        self.Ticker.start()

        self.Trader.stop()
        self.Trader.symbol = new_symbol
        self.Trader.a.config(text=new_title)
        self.Trader.b.config(text=new_sub)
        self.Trader.websocket = CryptoWS(
            stream=f"{new_symbol}@aggTrade", on_message=self.Trader.on_message)
        self.Trader.start()

        self.Book.stop()
        self.Book.symbol = new_symbol
        self.Book.a.config(text=new_title)
        self.Book.b.config(text=new_sub)
        self.Book.websocket = CryptoWS(
            stream=f"{new_symbol}@depth", on_message=self.Book.on_message)
        self.Book.start()

        self.Kline.symbol = new_symbol
        self.Kline.a.config(text=new_title)
        self.Kline.b.config(text=new_sub)
        self.Kline.render()
                
    def on_closing(self):
        '''Clean up for those websockets.'''
        self.Trader.stop()
        self.Ticker.stop()
        self.Book.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
