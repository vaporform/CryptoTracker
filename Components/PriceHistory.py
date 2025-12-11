import tkinter as tk
from tkinter import ttk

try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI


class PriceHistory(BaseUI.Widget):
    def __init__(self, parent, symbol, colors=[], title="", sub=""):
        super().__init__(parent, colors, middle="Price", title=title, subtitle=sub)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button

    def get_price_history(self):
        '''Fetch price history.'''
        price = CryptoREST().price(self.symbol.upper())
        print(price)
        return price


if __name__ == "__main__":
    root = tk.Tk()
    widget = PriceHistory(root, "btcusdt")
    widget.get_price_history()
    widget.pack()
    root.mainloop()
