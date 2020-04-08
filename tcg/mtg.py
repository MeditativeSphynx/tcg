import tkinter as tk

from loguru import logger


class MtgTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        logger.debug('>>> Setting up MtG Frame <<<')
        master.add(self, text='MtG')

        self.card_name_lbl = tk.Label(self, text='Card Name')
        self.card_name_lbl.pack()

        self.card_name_entry = tk.Entry(self, text='Placeholder')
        self.card_name_entry.pack()