import json
from datetime import datetime
import websocket


class OpenChain:

    def __init__(self, nodes: list) -> None:
        self.chain = []
        self.nodes = nodes

    def create_block(self, origin: str, amount: str, destination: str, signature: str) -> dict:
        """
        Creates new block and appends it to the blockchain
        :param amount: Resource of the block
        :param origin: Owner of the block
        :return: Newly created block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': 0,
            'previous_hash': '1',
            'origin': origin,
            'destination': destination,
            'amount': amount,
            'signature': signature
        }
        self.chain.append(block)
        # TODO: Broadcast block to all nodes
        return block

    def get_last_open_block(self) -> dict:
        if len(self.chain) < 1:
            return None
        last_open_block = self.chain[0]
        self.chain.remove(last_open_block)
        return last_open_block

    def __broadcast_block(self, block: dict):
        for node in self.nodes:
            ws = websocket.WebSocketApp(url='ws://' + str(node) + '/ws/new_open_block')
            ws.send(data=json.dumps(block))
