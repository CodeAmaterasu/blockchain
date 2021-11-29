import json

from fastapi import FastAPI
from data.blockchain import Blockchain

app = FastAPI()
blockchain = Blockchain()


@app.get('/api/mine_block')
async def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof=previous_proof)
    previous_hash = blockchain.hash_block(block=previous_block)

    block = blockchain.create_block(proof=proof, previous_hash=previous_hash)

    return {'message': 'Block mined successfully', 'block': str(json.dumps(block))}


@app.get('/api/get_chain')
async def get_chain():
    return {
        'chain': str(blockchain.chain),
        'chain_length': len(blockchain.chain)
    }


@app.get('/api/check_blockchain')
async def check_blockchain():
    return {
        'is_chain_valid': blockchain.is_chain_valid()
    }
