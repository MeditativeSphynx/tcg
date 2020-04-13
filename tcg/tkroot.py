import tkinter as tk
from tkinter.ttk import Notebook


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TCG')
        # self.geometry('500x500')
        self.notebook = Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)
