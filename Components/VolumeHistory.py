import tkinter as tk
from tkinter import ttk

try:
    from .CryptoHelper import *
    from . import BaseUI
except ImportError:
    from CryptoHelper import *
    import BaseUI


class VolumeHistory(BaseUI.Widget):
    def __init__(self, parent, symbol, colors=[], title="", sub=""):
        super().__init__(parent, colors, middle="Volume", title=title, subtitle=sub)
        target = self.frame
        self.symbol = symbol

    def get_volume_history(self):
        '''Fetch volume history.'''
        stats = CryptoREST().stat_24(self.symbol.upper())
        print(stats)
        return stats


if __name__ == "__main__":
    root = tk.Tk()
    widget = VolumeHistory(root, "btcusdt")
    widget.get_volume_history()
    widget.pack()
    root.mainloop()
