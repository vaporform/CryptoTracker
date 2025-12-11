import tkinter as tk
from tkinter import ttk

try:
    from .CryptoHelper import *
    from  . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI

class VolumeHistory(BaseUI.Widget):
    def __init__(self, parent, symbol, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        self.symbol = symbol
        # Title on same line as button
        ttk.Label(target, text=f"{self.symbol[:3].upper()}",
                  font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(target, text=f"{self.symbol[3:].upper()}",
                  font=("Arial", 8, "bold")).pack(side=tk.LEFT)

    def get_volume_history(self):
        """Fetch volume history."""
        stats = CryptoREST().stat_24(self.symbol)
        print(stats)
        return stats


if __name__ == "__main__":
    root = tk.Tk()
    widget = VolumeHistory(root, "btcusdt")
    widget.pack()
    root.mainloop()
