import json

from fastapi import FastAPI, WebSocket
from data.blockchain import Blockchain
from data.blockchain import Block
from data.openchain import OpenChain
from data.resources import Resources
import asyncio

app = FastAPI()
blockchain = Blockchain()
openchain = OpenChain()
resources = Resources()

new_block = False


@app.get('/api/mine_block')
async def mine_block():
    """
    Mine the oldest block in the openchain
    Returns message if the block was mined successfully
    """
    # TODO: Here we need to process pending blocks instead of creating a new one,
    #  so we have to keep track of not processed blocks
    # Get last open transaction
    last_transaction = openchain.get_last_open_block()
    if last_transaction is None:
        return {'message': 'No open blocks to mine'}
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof=previous_proof)
    previous_hash = blockchain.hash_block(block=previous_block)

    block = blockchain.create_block(proof=proof, previous_hash=previous_hash, owner=last_transaction['owner'], resource=
                                    last_transaction['resource'])
    global new_block
    new_block = True
    return {'message': 'Block mined successfully', 'block': str(json.dumps(block))}


@app.get('/api/get_chain')
async def get_chain():
    """
    Retrieve the current blockchain
    Returns the blockchain and it's current length
    """
    return {
        'chain': str(blockchain.chain),
        'chain_length': len(blockchain.chain)
    }


@app.get('/api/check_blockchain')
async def check_blockchain():
    """
    Checks if the blockchain is valid (which means it was not tampered with
    Returns a message with the validity of the chain
    """
    return {
        'is_chain_valid': blockchain.is_chain_valid()
    }


@app.post('/api/create_block')
async def create_block(block: Block):
    """
    Create a new block (this means a new transaction)
    Body: The new block by schema
    Returns message if block was created successfully
    """
    if block.resource == '':
        return {'message', 'Cannot create block with empty resource'}
    if resources.check_resource(block.resource):
        openchain.create_block(owner=block.owner, resource=resources.get_resource(block.resource))
        return {'message', 'New block created on the openchain'}
    else:
        return {'message', 'Resource does not exist'}


@app.get('/api/get_openchain')
async def get_openchain():
    """
    Retrieve the current openchain with non verified blocks
    Returns the chain and it's current length
    """
    return {
        'chain': str(openchain.chain),
        'chain_length': len(openchain.chain)
    }


@app.websocket('/ws/blockchain')
async def broadcast_blockchain(websocket: WebSocket):
    await websocket.accept()
    while True:
        # TODO: Do we really wanna broadcast the whole chain?
        await asyncio.sleep(5)
        await websocket.send_json(blockchain.chain)


@app.websocket('/ws/openchain')
async def broadcast_openchain(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(5)
        await websocket.send_json(openchain.chain)
