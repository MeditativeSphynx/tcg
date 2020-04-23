from tcg import logger
from tcg.pokenetwork import gen_id

from twisted.internet import protocol

import json


class PokeClient(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        print(data.decode('utf8'))

    def connectionMade(self):
        """Once a connection is made, send the node information"""
        
        data = json.dumps({
            'node_id': self.factory.node_client_id,
            'msg_type': 'new_connection'
        })

        self.transport.write(data.encode('utf8'))

    def close_connection(self):
        self.transport.loseConnection()


class PokeClientFactory(protocol.ClientFactory):
    def __init__(self, host, port):
        self.node_client_id = gen_id()
        self.connected_to_host = host
        self.connected_to_port = port

    def startedConnecting(self, connector):
        print(f'connecting to {self.connect_to_host}:{self.connect_to_port}')

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost', reason)

    def buildProtocol(self, addr):
        return PokeClient(self)
