import tkinter as tk

from loguru import logger

logger.add('../logs/debug.log', level='DEBUG')

class NetworkTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        logger.debug('setting up the network tab')

        master.add(self, text='PokeNetwork')

        # NOTE: WHAT OTHER NODE CONNECTIVITY VALUES ARE THERE?
        # node_status_values = [
        #   'connecting', 'connected', 'disconnected'
        # ]
        self.connected_status = tk.StringVar(self, value='disconnected')
        self.connected_lbl = tk.Label(self, text='Node:')
        self.connected_lbl.grid(column=0, row=0, sticky=('W'))
        self.connected_status_lbl = tk.Label(self, textvar=self.connected_status)
        self.connected_status_lbl.grid(column=1, row=0, sticky=('W'))

        self.server_lbl = tk.Label(self, text='Server:')
        self.server_lbl.grid(column=0, row=1, sticky=('W'))

        # NOTE: ARE THERE ANY OTHER VALUABLE SERVER STATUSES
        # server_status_values = [
        #   'listening', 'down', 'receiving', 'transmitting'
        # ]
        self.server_status = tk.StringVar(self, value='down')
        self.server_status_lbl = tk.Label(self, textvar=self.server_status)
        self.server_status_lbl.grid(column=1, row=1, sticky=('W'))

        self.server_start_btn = tk.Button(self, text='Start Server')
        self.server_start_btn.grid(
            column=0, row=5, sticky=('N', 'S', 'E', 'W'),
            columnspan=2
        )

        self.client_start_btn = tk.Button(self, text='Start Client')
        self.client_start_btn.grid(
            column=0, row=6, sticky=('N', 'S', 'E', 'W'),
            columnspan=2
        )