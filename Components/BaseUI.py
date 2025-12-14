import tkinter as tk
from tkinter import ttk

# The Father Of Everything


class Widget:
    '''
    The base class for creating widgets.
    '''

    def __init__(self, parent, title="Widget", subtitle="base", middle=None):
        self.parent = parent
        self.hiding = False

        # The base frame for storing the header and the content frame.
        self.widget_frame = tk.Frame(parent, borderwidth=2,relief=tk.RIDGE, padx=6, pady=6)

        # Create header here
        self.create_header(title,subtitle,middle)

        # Store stuff for the actual content
        self.frame = tk.Frame(self.widget_frame)
        self.frame.pack(side=tk.TOP, fill="both", expand=True)

        # Create UI here
        self.create_ui()

    def create_header(self,title,subtitle,middle):
        '''
        Initialize the header (aka. taskbar thing)
        '''

        # Style: [TITLE/SUBTITLE      MIDDLE_TEXT       CLOSE]
        self.header = tk.Frame(self.widget_frame)
        
        # Pack the close button to the right side.
        self.button = ttk.Button(self.header, text="Hide",width=5, command=self.hide)
        self.button.pack(side=tk.RIGHT)

        # Setting up the title and subtitle
        self.title_sub = tk.Frame(self.header)
        self.t = ttk.Label(self.title_sub, text=title, font=("Arial", 12, "bold"))
        self.s = ttk.Label(self.title_sub, text=subtitle, font=("Arial", 10, "bold"))

        self.t.grid(row=0, column=0, columnspan=2)
        self.s.grid(row=1, column=0, columnspan=2, sticky='w')

        # Pack the Title to the left side.
        self.title_sub.pack(side=tk.LEFT, fill=tk.BOTH)

        # Now, it is safe to pack the middle text.
        if middle is not None:
            c = ttk.Label(self.header, text=middle, font=(
                "Arial", 16, "bold"), anchor="center")
            c.pack(side=tk.LEFT, expand=True, fill="both")
        
        # Anf then, pack the header!
        self.header.pack(side=tk.TOP, fill="x")

    def create_ui(self):
        '''
        Dummy UI initializer. Always run when creates an instance. 
        Must edit this!
        '''

        pass

    def hide(self):
        '''
        Allow the widget to hide/unhide.
        '''
        if self.hiding:
            self.frame.pack(side=tk.TOP, fill="both", expand=True)
            self.frame.pack_configure(fill="both", expand=True)
            self.button.config(text="Hide")
        else:
            self.frame.pack_configure(fill="x", expand=False)
            self.frame.pack_forget()
            self.button.config(text="Show")
        self.hiding = not self.hiding

    def pack(self, **kwargs):
        '''
        Placing widget with pack method.
        '''

        self.widget_frame.pack(**kwargs)

    def grid(self, **kwargs):
        '''
        Placing widget with grid method.
        '''

        self.widget_frame.grid(**kwargs)

    def grid_forget(self):
        '''
        Unload widget via grid.
        '''

        self.widget_frame.grid_forget()

    def pack_forget(self):
        '''
        Unload widget via pack.
        '''

        self.widget_frame.pack_forget()


class TestWidget(Widget):
    def __init__(self, parent):
        super().__init__(parent)
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
    '''
    Testing the base widget components
    '''

    root = tk.Tk()
    widget = Widget(root, title="Boop", subtitle="101", middle="Hai!")
    widget.pack()
    root.mainloop()
