import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

try:
    from .CryptoHelper import *
    from  . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# REST
class KlineHistory(BaseUI.Widget):
    def __init__(self, parent,symbol, colors=[],title="",sub=""):
        super().__init__(parent, colors,middle="Kline",title=title,subtitle=sub)
        target = self.frame
        self.symbol = symbol

        # --- Matplotlib Canvas ---
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=target)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.render()

    def get_kline_history(self):
        """Fetch kline history."""
        klines = CryptoREST().kline(self.symbol.upper(), interval="1h", limit=48)
        return klines

    def render(self):
        """Fetch and display kline history using numpy and matplotlib."""
        klines = self.get_kline_history()
        if not klines:
            print("No kline data to plot.")
            return

        # Use numpy to process data (Open, High, Low, Close)
        # Indices: 1=Open, 2=High, 3=Low, 4=Close
        data = np.array(klines)[:, 1:5].astype(float)

        self.ax.clear()
        
        width = 0.6  # Width of the candlestick body
        
        for i, (o, h, l, c) in enumerate(data):
            color = 'green' if c >= o else 'red'
            
            # Draw the high-low wick
            self.ax.plot([i, i], [l, h], color=color, linewidth=1)
            
            # Draw the open-close body
            rect = patches.Rectangle(
                (i - width / 2, min(o, c)),
                width,
                abs(c - o),
                facecolor=color
            )
            self.ax.add_patch(rect)

        self.ax.set_title(f'Candlestick Chart')
        self.ax.set_ylabel('Price')
        self.ax.set_xlabel('Time')
        self.ax.autoscale_view()
        self.fig.tight_layout()
        self.canvas.draw()

    def start(self):
        self.parent.after(5000, self.render) # Update 5 seconds :)

if __name__ == "__main__":
    root = tk.Tk()
    widget = KlineHistory(root, "btcusdt")
    print(widget.get_kline_history())
    widget.pack()
    root.mainloop()
