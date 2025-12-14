import tkinter as tk
from tkinter import ttk
import json

try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# WEBSOCKET
class Ticker(BaseUI.Widget):
    '''
    A normal ticker widget that shows one symbol.
    '''

    def __init__(self, parent, symbol, title="", sub="",middle="Ticker"):
        super().__init__(parent, middle=middle, title=title, subtitle=sub)
        self.is_active = False
        self.symbol = symbol
        self.websocket = CryptoWS(stream=f"{self.symbol}@ticker",on_message=self.on_message)

    def create_ui(self):
        '''
        Initialize the interface for the ticker.
        '''

        target = self.frame

        self.price_label = tk.Label(target, text="--,---",font=("Arial", 24, "bold"))
        self.change_label = ttk.Label(target, text="--",font=("Arial", 12))

        self.price_label.pack()
        self.change_label.pack()
        
    def on_message(self, ws, message):
        '''
        Handle price updates.
        '''
        
        if not self.is_active:
            return

        data = json.loads(message)
        price = float(data["c"])
        change = float(data["p"])
        percent = float(data["P"])

        # Schedule GUI update on main thread
        self.parent.after(0, self.update_display, price, change, percent)

    def update_display(self, price, change, percent):
        '''
        Update the ticker display.
        '''
        
        if not self.is_active:
            return

        color,sign = "",""
        
        if change >= 0:
            color = "green"
            sign = "+"
        else:
            color = "red"
            sign = "-"

        self.price_label.config(text=f"{price:,.2f}", foreground=color)
        self.change_label.config(text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",foreground=color)

    def start(self):
        '''
        Start the ticker updates.
        '''

        if self.is_active:
            return

        self.is_active = True
        self.websocket.start()

    def stop(self):
        '''
        Stop the ticker updates.
        '''

        if not self.is_active:
            return

        self.is_active = False
        self.websocket.close()


class MiniTicker(BaseUI.Widget):
    '''
    A list ticker widget that shows all symbols from an array.
    '''

    def __init__(self, parent, symbols, middle="Mini Ticker"):
        super().__init__(parent, middle=middle, title="", subtitle="")
        self.is_active = False
        self.ws_a = [] # [[sym,ws,[price,change]], ... ]
        self.create_ws(symbols)
        
    def create_ws(self,ws_list):
        for i, symbol in enumerate(ws_list):
            ws = CryptoWS(stream=f"{symbol}@ticker",
                                  on_message=self.on_message)
            n = [symbol,ws,self.create_mini_ui(i,symbol)]
            self.ws_a.append(n)
     
    def create_mini_ui(self,index,name):
        '''
        Initialize the interface for the ticker.
        '''

        target = self.frame

        tk.Label(target, text=name.upper(),font=("Arial", 10,"bold")).grid(row=index,column=0,padx=5)

        price_label = tk.Label(target, text="--,---",font=("Arial", 10))
        price_label.grid(row=index,column=1,padx=5)

        # Change
        change_label = ttk.Label(target, text="--",font=("Arial", 10))
        change_label.grid(row=index,column=2,padx=5)
        
        return price_label,change_label
        
    def on_message(self, ws, message):
        '''
        Handle price updates.
        '''

        if not self.is_active:
            return

        data = json.loads(message)

        # find which socket sent the message :P
        for item in self.ws_a:
            if item[1].ws == ws:
                price = float(data["c"])
                change = float(data["p"])
                percent = float(data["P"])

                # Schedule GUI update on main thread
                self.parent.after(0, self.update_display, price, change, percent,item[2])
                break
    
    def update_display(self, price, change, percent,labels):
        '''
        Update the ticker display.
        '''

        if not self.is_active:
            return
        price_label,change_label = labels
        color,sign = "",""
        
        if change >= 0:
            color = "green"
            sign = "+"
        else:
            color = "red"
            sign = "-"

        price_label.config(text=f"{price:,.2f}", foreground=color)
        change_label.config(text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",foreground=color)

    def start(self):
        '''
        Start the ticker updates.
        '''
        
        if self.is_active:
            return
        self.is_active = True
        for i in self.ws_a:
            i[1].start()

    def stop(self):
        '''
        Stop the ticker updates.
        '''
        
        if not self.is_active:
            return
        self.is_active = False
        for item in self.ws_a:
            item[1].close()


if __name__ == "__main__":
    '''
    Testing the ticker widgets.
    '''

    root = tk.Tk()
    ticker = Ticker(root, "btcusdt")
    ticker.pack()
    ticker.start()

    mini = MiniTicker(root,["ethusdt","btcusdt"])
    mini.pack()
    mini.start()
    root.mainloop()
