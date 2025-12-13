import tkinter as tk
from tkinter import ttk

try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# WEBSOCKET


class Book(BaseUI.Widget):
    def __init__(self, parent, symbol, title="", sub=""):
        super().__init__(parent, middle="Book", title=title, subtitle=sub)
        target = self.frame
        self.symbol = symbol
        self.is_active = False

        col_width = 100
        self.ask_tree = ttk.Treeview(target, columns=(
            "Ask", "Quantity"), show='headings', height=10)
        self.ask_tree.column("Ask", width=col_width, minwidth=50)
        self.ask_tree.column("Quantity", width=col_width, minwidth=50)

        self.ask_tree.heading("Ask", text="Ask")
        self.ask_tree.heading("Quantity", text="Quantity")

        self.bid_tree = ttk.Treeview(target, columns=(
            "Bid", "Quantity"), show='headings', height=10)
        self.bid_tree.column("Bid", width=col_width, minwidth=50)
        self.bid_tree.column("Quantity", width=col_width, minwidth=50)

        self.bid_tree.heading("Bid", text="Bid")
        self.bid_tree.heading("Quantity", text="Quantity")

        self.ask_tree.tag_configure('Ask', foreground='red')
        self.bid_tree.tag_configure('Bid', foreground='green')

        self.ask_tree.pack()
        self.bid_tree.pack()

        self.websocket = CryptoWS(stream=f"{self.symbol}@depth",
                                  on_message=self.on_message,
                                  on_error=lambda ws,
                                  err: print(f"{self.symbol} error: {err}"),
                                  on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
                                  on_open=lambda ws: print(f"{self.symbol} connected")
                                  )

    def render(self, bids, asks):
        '''
        Renders the Order Book by clearing and repopulating two separate 
        Treeview widgets for Asks (Sells) and Bids (Buys).
        '''
        # print("Rendering Book Update...")

        # --- 1. Render ASKS (Sells / Red) ---

        # Asks should be ordered from the lowest price (best price to sell) down to higher prices.
        # The lowest ask is at the top, closest to the spread.

        # Clear old data
        for row in self.ask_tree.get_children():
            self.ask_tree.delete(row)

        # Insert new asks: highest price at the bottom of the visible section
        # Note: We reverse the order of the asks for proper visual display
        # (Lowest ask at the top of the treeview)
        for price, qty in reversed(asks):
            # We assume tags ('ask') are configured in __init__
            self.ask_tree.insert("", tk.END, values=(
                f"{float(price):,.2f}", f"{float(qty):.6f}"), tags=('Ask',))

        # --- 2. Render BIDS (Buys / Green) ---

        # Bids should be ordered from the highest price (best price to buy) down to lower prices.
        # The highest bid is at the top, closest to the spread.

        # Clear old data
        for row in self.bid_tree.get_children():
            self.bid_tree.delete(row)

        # Insert new bids: highest price at the top of the treeview
        for price, qty in bids:
            # We assume tags ('bid') are configured in __init__
            self.bid_tree.insert("", tk.END, values=(
                f"{float(price):,.2f}", f"{float(qty):.6f}"), tags=('Bid',))

    def on_message(self, ws, message):
        '''Handle price updates.'''
        if not self.is_active:
            return

        data = json.loads(message)
        bids = data['b']
        asks = data['a']

        # Schedule GUI update on main thread
        self.parent.after(0, self.render, bids, asks)

    def start(self):
        '''Start the ticker updates.'''
        if self.is_active:
            return
        self.is_active = True
        self.websocket.start()

    def stop(self):
        '''Stop the ticker updates.'''
        if not self.is_active:
            return
        self.is_active = False
        self.websocket.close()


if __name__ == "__main__":

    root = tk.Tk()
    widget = Book(root, "btcusdt")
    widget.pack()
    widget.start()  # Refresh every 1 second
    root.mainloop()
