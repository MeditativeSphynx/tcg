import tkinter as tk
from tkinter.ttk import Notebook

from twisted.internet import reactor


class Root(tk.Tk):
    def __init__(self, reactor):
        super().__init__()
        
        self.reactor = reactor

        self.title('TCG')
        # self.geometry('500x500')
        self.notebook = Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)

    def shutdown_callback(self):
        if tk.messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
            self.reactor.stop()
            self.destroy()