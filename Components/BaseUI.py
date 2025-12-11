import tkinter as tk
from tkinter import ttk

# The Father Of Everything
class Widget:
    def __init__(self,parent,colors=[]):
        self.parent = parent
        self.colors = colors
        self.frame = tk.Frame(parent,borderwidth=2,relief=tk.RIDGE)
        self.button = ttk.Button(self.frame, text="Close")
        self.button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def pack(self, **kwargs):
        """Allow easy placement of ticker."""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Hide the ticker."""
        self.frame.pack_forget()

class TestWidget(Widget):
    def __init__(self, parent, colors=[]):
        super().__init__(parent, colors)
        target = self.frame
        ttk.Label(target, text="Hello World", 
                 font=("Arial", 16, "bold")).pack()

        ttk.Label(target, text="Hello World", 
                 font=("Arial", 16, "bold")).pack()

        ttk.Label(target, text="Hello World", 
                 font=("Arial", 16, "bold")).pack()

        ttk.Label(target, text="Hello World", 
                 font=("Arial", 16, "bold")).pack()

if __name__ == "__main__":
    
    root = tk.Tk()
    widget = Widget(root)
    widget.pack()
    root.mainloop()
