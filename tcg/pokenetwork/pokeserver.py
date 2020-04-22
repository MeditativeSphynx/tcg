from twisted.internet import protocol

from tcg import logger
from tcg.pokenetwork import gen_id

import json


class PokeServer(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.peer = {
            'node_id': None,
            'verified': False,
            'host': None,
            'connected': False
        }

    def connectionMade(self):
        logger.info(f'{self.transport.getPeer().host} connected')
        self.peer.update({
            'host': self.transport.getPeer().host
        })

    def connectionLost(self, reason):
        logger.info(f'{self.transport.getPeer().host} disconnected')
        self.factory.connected_peers.remove(self.peer)
        logger.debug(
            f'number of connected peers: {len(self.factory.connected_peers)}'
        )

    def dataReceived(self, data):
        d = json.loads(data)
        if d['msg_type'] == 'poke_transfer':
            print('incoming transfer')
        elif d['msg_type'] == 'new_connection':
            self.setup_new_peer(d)
    
    def setup_new_peer(self, data):
        self.peer.update({
            'node_id': data['node_id'],
            'verified': True,
            'connected': True,
            'self': self.node_is_self(data['node_id'])
        })
        self.factory.connected_peers.append(self.peer)
        logger.debug(
            f'number of connected peers: {len(self.factory.connected_peers)}'
        )

    def node_is_self(self, node_id):
        if node_id == self.factory.node_id:
            return True
        else:
            return False

class PokeServerFactory(protocol.Factory):
    def __init__(self):
        self.node_id = gen_id()
        self.connected_peers = []

    def buildProtocol(self, addr):
        logger.info('building the server protocol')
        return PokeServer(self)

    def startedConnecting(self, connector):
        print('strating connection')