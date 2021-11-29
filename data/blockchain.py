import json
from datetime import datetime
from hashlib import sha256


# noinspection PyMethodMayBeStatic
class Blockchain:

    def __init__(self) -> None:
        # FIXME: https://www.section.io/engineering-education/how-to-create-a-blockchain-in-python/ used this tutorial
        # List containing all blocks of the chain
        self.chain = []
        # Creating the gensis block (first block of the chain)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof: int, previous_hash: str) -> dict:
        # TODO: Might wanna move the block of the chain to a own class instead of using a dictionary
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        # Default the proof ain't checked
        check_proof = False
        while check_proof is False:
            hash_operation = sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_block(self, block: dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain: list):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = block['proof']

            hash_operation = sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
