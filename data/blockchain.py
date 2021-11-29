import json
from datetime import datetime
from hashlib import sha256


# noinspection PyMethodMayBeStatic
class Blockchain:
    """
    Class for the blockchain
    """

    def __init__(self) -> None:
        # FIXME: https://www.section.io/engineering-education/how-to-create-a-blockchain-in-python/ used this tutorial
        # List containing all blocks of the chain
        self.chain = []
        # Creating the gensis block (first block of the chain)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof: int, previous_hash: str) -> dict:
        """
        Creates new block and appends it to the blockchain
        :param proof: Proof of the block
        :param previous_hash: Hash to the previous block
        :return: Newly created block
        """
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
        """
        Method for mining new blocks
        :param previous_proof: Proof of the previous block
        :return: Proof of work for new block
        """
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
        """
        Create hash for block in blockchain
        :param block: Block to hash
        :return: Hexdigest of the hashed block
        """
        encoded_block = json.dumps(block, sort_keys=True).encode('utf-8')
        print('hashing block..')
        print(type(encoded_block))
        return sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        """
        Check if the blockchain is valid
        :return: Boolean if the chain is valid
        """
        # Copy the chain first because live changes could hypothetically be made
        chain = self.chain
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
