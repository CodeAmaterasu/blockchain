import json

from fastapi import FastAPI
from data.blockchain import Blockchain
from data.blockchain import Block
from data.openchain import OpenChain
from data.resources import Resources
app = FastAPI()
blockchain = Blockchain()
openchain = OpenChain()
resources = Resources()


@app.get('/api/mine_block')
async def mine_block():
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


@app.post('/api/create_block')
async def create_block(block: Block):
    if block.resource == '':
        return {'message', 'Cannot create block with empty resource'}
    if resources.check_resource(block.resource):
        openchain.create_block(owner=block.owner, resource=resources.get_resource(block.resource))
    else:
        return {'message', 'Resource does not exist'}


@app.get('/api/get_openchain')
async def get_openchain():
    return {
        'chain': str(openchain.chain),
        'chain_length': len(openchain.chain)
    }
