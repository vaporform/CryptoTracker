import tkinter as tk
from tkinter import ttk
from datetime import datetime

import json
try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# WEBSOCKET


class TradeHistory(BaseUI.Widget):
    '''
    A widget to show you trade history!
    '''

    def __init__(self, parent, symbol, colors=[], title="", sub=""):
        super().__init__(parent, colors, middle="Trades", title=title, subtitle=sub)
        target = self.frame
        self.symbol = symbol
        self.is_active = False
        self.websocket = CryptoWS(stream=f"{self.symbol}@aggTrade", on_message=self.on_message, on_error=lambda ws, err: print(f"{self.symbol} error: {err}"), on_close=lambda ws, s, m: print(f"{self.symbol} closed"), on_open=lambda ws: print(f"{self.symbol} connected")
                                  )

        # Trade history table
        columns = ('time', 'price', 'quantity')
        self.tree = ttk.Treeview(target, columns=columns, show='headings')

        # Define headings
        self.tree.heading('time', text='Time')
        self.tree.heading('price', text='Price')
        self.tree.heading('quantity', text='Quantity')

        # Configure column widths
        self.tree.column('time', width=100)
        self.tree.column('price', width=100)
        self.tree.column('quantity', width=100)

        self.tree.tag_configure('buy', foreground='green')
        self.tree.tag_configure('sell', foreground='red')

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_message(self, ws, message):
        '''Handle price updates.'''
        if not self.is_active:
            return

        data = json.loads(message)

        # Schedule GUI update on main thread
        self.parent.after(0, self.update_display, data)

    def update_display(self, data):
        '''Update the ticker display.'''
        if not self.is_active:
            return

        trade_time = datetime.fromtimestamp(data['T'] / 1000).strftime('%H:%M:%S')
        price = float(data['p'])
        quantity = float(data['q'])
        side = 'buy' if data['m'] else 'sell'

        self.tree.insert('', 0, values=(
            trade_time, f"{price:,.2f}", f"{quantity:.4f}"), tags=(side,))

        # Limit to 20 items
        if len(self.tree.get_children()) > 20:
            self.tree.delete(self.tree.get_children()[-1])

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
    widget = TradeHistory(root, "btcusdt")
    widget.start()
    widget.pack()
    root.mainloop()
