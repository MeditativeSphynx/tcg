import tkinter as tk

from twisted.internet import endpoints

from tcg.pokenetwork import pokeserver, pokeclient
from tcg import log_path, logger


class NetworkTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__()
        logger.debug('setting up the network tab')

        self.root = master
        self.master = self.root.notebook

        self.bootstrap_nodes = (
            {'host': 'localhost', 'port': 8000},
        )

        self.master.add(self, text='PokeNetwork')

        # NOTE: WHAT OTHER NODE CONNECTIVITY VALUES ARE THERE?
        # node_status_values = [
        #   'connecting', 'connected', 'disconnected'
        # ]
        self.connected_status = tk.StringVar(self, value='disconnected')
        self.connected_lbl = tk.Label(self, text='Node:')
        self.connected_lbl.grid(column=0, row=0, sticky=('W'))
        self.connected_status_lbl = tk.Label(self, 
                                             textvar=self.connected_status)
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

        self.client_start_btn = tk.Button(
            self, text='Start Client', command=self.start_node
        )
        self.client_start_btn.grid(
            column=0, row=5, sticky=('N', 'S', 'E', 'W'),
            columnspan=2
        )

        self.server_start_btn = tk.Button(
            self, text='Start Server', command=self.start_server
        )
        self.server_start_btn.grid(
            column=0, row=6, sticky=('N', 'S', 'E', 'W'),
            columnspan=2
        )

    # TODO: SETUP THE NODE CONNECTION LOGIC
    # TODO: SETUP THE NODE CODE
    def start_node(self):
        for node_addr in self.bootstrap_nodes:
            host, port = node_addr.values()
            
            pokeclient_factory = pokeclient.PokeClientFactory(host, port)

            endpoint = endpoints.TCP4ClientEndpoint(
                self.root.reactor,
                host=host,
                port=port
            )

            poke_client_connect = endpoints.connectProtocol(
                endpoint=endpoint, 
                protocol=pokeclient.PokeClient(
                    factory=pokeclient_factory
                )
            )
            logger.debug(f'connecting to {host}:{port}')

    def start_server(self):
        logger.info('starting server')
        listener = endpoints.TCP4ServerEndpoint(self.root.reactor, port=8000)
        listener.listen(pokeserver.PokeServerFactory())