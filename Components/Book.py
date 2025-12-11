import tkinter as tk
from tkinter import ttk

try:
    from .CryptoHelper import *
    from  . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

#REST
class Book(BaseUI.Widget):
    def __init__(self, parent, symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}",
                  font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
                  font=("Arial", 8, "bold")).pack(side=tk.LEFT)

        self.treeview = ttk.Treeview(target, columns=("Price", "Quantity"), show='headings', height=15)
        self.treeview.heading("Price", text="Price")
        self.treeview.heading("Quantity", text="Quantity")
        self.render()
        
    def get_book(self,limit=10):
        """Fetch order book."""
        book = CryptoREST().book_depth(self.symbol.upper(), limit=limit)
        
        #print("GOT BOOK!",book)
        return book

    def render(self):
        """Fetch and display the latest book."""
        print("Rendering Book...")
        book = self.get_book()
        if not book or "bids" not in book or "asks" not in book:
            return

        # Clear current rows
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Add asks (in reverse for correct order)
        for price, qty in reversed(book.get("asks", [])):
            self.treeview.insert("", tk.END, values=(price, qty), tags=('ask',))

        # Add a separator
        self.treeview.insert("", tk.END, values=("-----", "-----"))

        # Add bids
        for price, qty in book.get("bids", []):
            self.treeview.insert("", tk.END, values=(price, qty), tags=('bid',))

        # Style the rows
        self.treeview.tag_configure('bid', foreground='green')
        self.treeview.tag_configure('ask', foreground='red')
        self.treeview.pack()
    
    def update_interval(self, interval_ms=1000):
        """Update the book display at regular intervals."""
        self.render()
        self.frame.after(interval_ms, self.update_interval, interval_ms)
    
if __name__ == "__main__":
    
    root = tk.Tk()
    widget = Book(root, "btcusdt")
    widget.pack()
    widget.update_interval(1000)  # Refresh every 1 second
    root.mainloop()
