import tkinter as tk
from tkinter import ttk

# The Father Of Everything


class Widget:
    def __init__(self, parent, colors=[], title="Widget", subtitle="base", middle=None):
        self.parent = parent
        self.colors = colors
        self.active = False

        self.frame = tk.Frame(parent, borderwidth=2,
                              relief=tk.RIDGE, padx=10, pady=10)
        self.header = tk.Frame(self.frame)

        # 1. Pack the Button to the RIGHT
        self.button = ttk.Button(self.header, text="Close", command=self.hide)
        self.button.pack(side=tk.RIGHT, padx=5)

        # 2. Setup the Title (Left side) - DO NOT PACK YET
        self.cute = tk.Frame(self.header)
        self.a = ttk.Label(self.cute, text=title, font=("Arial", 16, "bold"))
        self.b = ttk.Label(self.cute, text=subtitle, font=("Arial", 8, "bold"))

        self.a.grid(row=0, column=0, columnspan=2)
        self.b.grid(row=1, column=0, columnspan=2, sticky='w')

        # 3. Pack the Title to the LEFT
        self.cute.pack(side=tk.LEFT, fill=tk.BOTH)

        # 4. Pack the Middle Label LAST
        # expand=True makes it claim all the empty space between Left and Right
        # anchor="center" ensures the text sits in the middle of that space
        if middle is not None:
            c = ttk.Label(self.header, text=middle, font=(
                "Arial", 16, "bold"), anchor="center")
            c.pack(side=tk.LEFT, expand=True, fill="both")

        self.header.pack(side=tk.TOP, fill='x', expand=False)

    def hide(self):
        if self.active:
            self.pack_forget()
        else:
            self.pack()
        self.active = not self.active

    def pack(self, **kwargs):
        '''Allow easy placement of ticker.'''
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        '''Allow easy placement of ticker.'''
        self.frame.grid(**kwargs)

    def grid_forget(self):
        self.frame.grid_forget()

    def pack_forget(self):
        '''Hide the ticker.'''
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
    widget = Widget(root, title="Boop", subtitle="101", middle="Hai!")
    widget.pack()
    root.mainloop()
