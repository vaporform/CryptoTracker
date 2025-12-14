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
    '''
    A basic book widget
    '''

    def __init__(self, parent, symbol, title="", sub=""):
        super().__init__(parent, middle="Book", title=title, subtitle=sub)
        self.symbol = symbol
        self.is_active = False
        self.websocket = CryptoWS(stream=f"{self.symbol}@depth",on_message=self.on_message)
    
    def create_ui(self):
        '''
        UI initializer. Always run when creates an instance. 
        '''
        target = self.frame
        col_width = 100
        self.ask_tree = ttk.Treeview(target, columns=("Ask", "Quantity"), show="headings")
        self.ask_tree.column("Ask", width=col_width, minwidth=50)
        self.ask_tree.column("Quantity", width=col_width, minwidth=50)

        self.ask_tree.heading("Ask", text="Ask (Low to High)")
        self.ask_tree.heading("Quantity", text="Quantity")

        self.bid_tree = ttk.Treeview(target, columns=("Bid", "Quantity"), show="headings")
        self.bid_tree.column("Bid", width=col_width, minwidth=50)
        self.bid_tree.column("Quantity", width=col_width, minwidth=50)

        self.bid_tree.heading("Bid", text="Bid (High to Low)")
        self.bid_tree.heading("Quantity", text="Quantity")

        self.ask_tree.tag_configure("Ask", foreground="red")
        self.bid_tree.tag_configure("Bid", foreground="green")

        self.ask_tree.pack(expand=True, fill="both")
        self.bid_tree.pack(expand=True, fill="both")

        
    def render(self, bids, asks):
        '''
        Renders the order book.
        '''

        # First, clear both ask and bid tree.
        for row in self.ask_tree.get_children():
            self.ask_tree.delete(row)
        
        for row in self.bid_tree.get_children():
            self.bid_tree.delete(row)

        # ASK (Selling), the lowest price must be on TOP.
        for price, qty in asks:
            line = f"{float(price):,.2f}",f"{float(qty):.6f}"
            self.ask_tree.insert("", tk.END, values=line, tags=("Ask",))

        # Now, for the BIDS (Buying), we can simply plug in. The value are sorted to highest already.
        for price, qty in bids:
            line = f"{float(price):,.2f}",f"{float(qty):.6f}"
            self.bid_tree.insert("", tk.END, values=line, tags=("Bid",))

    def on_message(self, ws, message):
        '''
        Handle price updates.
        '''

        if not self.is_active:
            return

        data = json.loads(message)
        bids = data["b"]
        asks = data["a"]

        # Schedule GUI update on main thread
        self.parent.after(0, self.render, bids, asks)

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


if __name__ == "__main__":
    '''
    Testing the book widget
    '''

    root = tk.Tk()
    widget = Book(root, "btcusdt")
    widget.pack()
    widget.start()  # Refresh every 1 second
    root.mainloop()
