import json
from datetime import datetime
from hashlib import sha256


class OpenChain:

    def __init__(self) -> None:
        self.chain = []

    def create_block(self, owner: str, resource: str, signature: str) -> dict:
        """
        Creates new block and appends it to the blockchain
        :param resource: Resource of the block
        :param owner: Owner of the block
        :return: Newly created block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': 0,
            'previous_hash': '1',
            'owner': owner,
            'resource': resource,
            'signature': signature
        }
        self.chain.append(block)
        return block

    def get_last_open_block(self) -> dict:
        if len(self.chain) < 1:
            return None
        last_open_block = self.chain[0]
        self.chain.remove(last_open_block)
        return last_open_block
