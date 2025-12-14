import tkinter as tk
from tkinter import ttk

from Components.Ticker import Ticker, MiniTicker
from Components.Book import Book
from Components.TradeHistory import TradeHistory
from Components.KlineHistory import KlineHistory
from Components.CryptoHelper import CryptoWS

class Application:
    def __init__(self, root):
        self.cryptos = [
            "btcusdt",
            "dogeusdt",
            "ethusdt",
            "solusdt",
            "trxusdt",
            "xrpusdt",
        ]
        self.new_symbol = "btcusdt"
        self.root = root
        self.root.title("Crypto Dashboard")
        self.root.geometry("1280x720")
        
        # --- Main Container ---
        mainframe = ttk.Frame(root, padding=10)
        mainframe.pack(fill=tk.BOTH, expand=True)

        # Configure grid resizing
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=2)
        mainframe.columnconfigure(2, weight=1)
        
        mainframe.rowconfigure(0, weight=0)
        mainframe.rowconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)
        mainframe.rowconfigure(3, weight=1)
        mainframe.rowconfigure(4, weight=1)

        # WIDGET STUFF DOWN HERE!
        self.selected_crypto = tk.StringVar(self.root)
        self.selected_crypto.set(self.cryptos[0]) # default value
        
        # Row 0, Col 0: Options Menu
        self.Options = ttk.OptionMenu(mainframe, self.selected_crypto, self.selected_crypto.get(), *self.cryptos)
        self.Options.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=(0, 5))
        
        # Row 1, Col 0: Ticker 1
        self.Ticker = Ticker(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Ticker.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=(0, 2))
        # Row 2, Col 0: Ticker 2
        self.MiniTicker = MiniTicker(mainframe, self.cryptos)
        self.MiniTicker.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=(0, 2))
        # Row 4, Col 0: Trade History
        self.Trader = TradeHistory(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Trader.grid(row=3, column=0, sticky="nsew",pady=(2, 0), padx=(0, 5))

        # Row 0, Col 1: Kline History (Spans 5 rows)
        self.Kline = KlineHistory(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Kline.grid(row=0, column=1, rowspan=5, sticky="nsew", padx=5)
        
        # Row 0, Col 2: Book (Spans 5 rows)
        self.Book = Book(mainframe, "btcusdt", title="BTC", sub="USDT")
        self.Book.grid(row=0, column=2, rowspan=5, sticky="nsew")
        
        self.selected_crypto.trace_add("write", self.on_crypto_select)
        
        self.MiniTicker.start()
    
    def change_crypto(self, new_symbol):
        '''
        Change the current crypto symbol for all widgets.
        '''
        if new_symbol not in self.cryptos:
            print("Invalid symbol:", new_symbol)
            return
        self.new_symbol = new_symbol
        new_title = self.new_symbol.replace("usdt", "").upper()
        new_sub = "USDT"

        self.Ticker.symbol = self.new_symbol
        self.Ticker.t.config(text=new_title)
        self.Ticker.s.config(text=new_sub)
        self.Ticker.websocket = CryptoWS(
            stream=f"{self.new_symbol}@ticker", on_message=self.Ticker.on_message)
        
        self.Trader.symbol = self.new_symbol
        self.Trader.t.config(text=new_title)
        self.Trader.s.config(text=new_sub)
        self.Trader.websocket = CryptoWS(
            stream=f"{self.new_symbol}@aggTrade", on_message=self.Trader.on_message)
        
        self.Book.symbol = self.new_symbol
        self.Book.t.config(text=new_title)
        self.Book.s.config(text=new_sub)
        self.Book.websocket = CryptoWS(
            stream=f"{self.new_symbol}@depth", on_message=self.Book.on_message)
        
        self.Kline.symbol = self.new_symbol
        self.Kline.t.config(text=new_title)
        self.Kline.s.config(text=new_sub)
        
        # Reboot time!
        self.Kline.render() # Override
        self.start_widgets()
        
    def on_crypto_select(self, *args):
        '''
        Callback for when a new crypto is selected from the dropdown.
        '''

        self.stop_widgets()
        self.change_crypto(self.selected_crypto.get())
                
    def on_closing(self):
        '''
        Clean up for those websockets and saving.
        '''
        
        self.save_preferences()
        self.MiniTicker.stop()
        self.stop_widgets()
        
        self.root.destroy()
        
    def save_preferences(self):
        '''
        Save user preferences to a file.
        '''

        l = [
            "selected_crypto:"+str(self.new_symbol)+"\n",
            "Ticker:"+str(self.Ticker.hiding)+"\n",
            "Trader:"+str(self.Trader.hiding)+"\n",
            "Book:"+str(self.Book.hiding)+"\n",
            "Kline:"+str(self.Kline.hiding)+"\n",
            "MiniTicker:"+str(self.MiniTicker.hiding)
        ]
        with open("preferences.txt", "w") as f:
            f.writelines(l)
        pass  # Implement saving logic here
    
    def load_preferences(self):
        '''
        Load user preferences from a file.
        '''
        
        try:
            with open("preferences.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    
                    l = line.strip().split(":")
                    if len(l) != 2:
                        continue
                    key, value = l[0], l[1]
                    if key == "Ticker" and value == "True":
                        self.Ticker.hide()
                    elif key == "Trader" and value == "True":
                        self.Trader.hide()
                    elif key == "Book" and value == "True":
                        self.Book.hide()
                    elif key == "Kline" and value == "True":
                        self.Kline.hide()
                    elif key == "MiniTicker" and value == "True":
                        self.MiniTicker.hide()
                    elif key == "selected_crypto":
                        if value in self.cryptos:
                            self.selected_crypto.set(value)
                            # Don't call change_crypto here - it will be called when widgets start
    
        except FileNotFoundError:
            pass  # No preferences file found. Skip.
        
    def stop_widgets(self):
        '''
        Stop all the application's widgets.
        '''
        
        self.Book.stop()
        self.Trader.stop()
        self.Ticker.stop()
        
    def start_widgets(self):
        '''
        Start all the application's widgets.
        '''
        
        self.Book.start()
        self.Trader.start()
        self.Kline.start()
        self.Ticker.start()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.load_preferences()
    app.start_widgets()
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()