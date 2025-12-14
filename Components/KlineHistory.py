import tkinter as tk
from tkinter import ttk
from datetime import datetime

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import matplotlib.patheffects as pe

try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

# REST
class KlineHistory(BaseUI.Widget):
    '''
    Widget that show you graphs about the current market.
    '''

    def __init__(self, parent, symbol, title="", sub=""):
        super().__init__(parent, middle="Kline", title=title, subtitle=sub)
        self.symbol = symbol
        
        # Jumpstart the render.
        self.render()
        
    def create_ui(self):
        '''
        UI initializer. Always run when creates an instance. 
        '''

        target = self.frame

        # The candle on top...
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=target)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # The "overall" on bottom.
        self.fig2 = Figure(figsize=(6, 1), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=target)
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def get_kline_history(self):
        '''
        Fetch kline history.
        '''

        klines = CryptoREST().kline(self.symbol.upper(), interval="1h", limit=48)
        return klines

    def render(self):
        '''
        Display kline history using numpy and matplotlib.
        '''
        
        klines = self.get_kline_history()
        if not klines:
            print("No kline data to plot.")
            return
        # klines = [
        #           [0:TIME,1:OPEN,2:HIGH,3:LOW,4:CLOSE],
        #           .... ]

        # Extract timestamps then convert to datetime for each interval.
        ts = [datetime.fromtimestamp(i[0] / 1000) for i in klines]
        
        # Use numpy to process data (Open, High, Low, Close)
        data = np.array(klines)[:, 1:5].astype(float)
        vol_data = np.array(klines)[:, 5].astype(float)

        # Unload the graphs.
        self.ax.clear()
        self.ax2.clear()
        
        width = 0.6  # Width of the candlestick body
        colors = [] # For the bottom chart.
        
        for i, (Open, High, Low, Close) in enumerate(data):
            color = ""
            if Close >= Open:
                color = "green"
            else:
                color = "red"
            
            colors.append(color)

            # Draw the high-low wick
            self.ax.plot([i, i], [Low, High], color=color, linewidth=1)

            # Draw the open-close body
            rect = patches.Rectangle(
                (i - width / 2, min(Open, Close)),
                width,
                abs(Close - Open),
                facecolor=color
            )
            self.ax.add_patch(rect)
            
            # Now, draw the overalls.
            self.ax2.bar(range(len(vol_data)), vol_data, color=colors)
            
        # Lastly, draw the line where the price is as of now.
        self.ax.axhline(data[-1, 3], color="blue", linestyle="--", linewidth=1)
        self.ax.text(0, data[-1, 3], f"{data[-1, 3]:.2f}", color="blue", va="bottom", ha="left",
                    path_effects=[pe.withStroke(linewidth=4, foreground="white")])
        self.ax.grid(True)
        self.ax.set_ylabel("Price")
        self.ax.get_xaxis().set_visible(False)
        self.ax.autoscale_view()
        self.ax.title.set_text(f"Candlestick Chart 1h interval")
        self.fig.tight_layout()
        
        # Show a label for every 6th hour to prevent clutter
        tick_spacing = 6
        tick_labels = [tsi.strftime("%H:%M") for tsi in ts]
        
        self.ax2.set_xticks(np.arange(0, len(tick_labels), tick_spacing))
        self.ax2.set_xticklabels(tick_labels[::tick_spacing], rotation=30, ha="right")

        self.ax2.grid(True)
        self.ax2.set_ylabel("Volume")
        self.ax2.autoscale_view()
        self.fig2.tight_layout()
        self.canvas.draw()
        self.canvas2.draw()

    def start(self):
        '''
        Start the rendering.
        '''
        
        self.render()
        self.parent.after(60000, self.start)  # Reschedule itself for continuous updates

if __name__ == "__main__":
    '''
    Testing the kline widget.
    '''

    root = tk.Tk()
    widget = KlineHistory(root, "btcusdt")
    print(widget.get_kline_history())
    widget.pack()
    root.mainloop()
