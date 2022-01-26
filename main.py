import json
from pydoc import describe

from ecdsa import SECP256k1, SigningKey
from fastapi import FastAPI, WebSocket
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from data.blockchain import Blockchain
from data.blockchain import Block
from data.openchain import OpenChain
from data.token import TokenPool
import asyncio
import ecdsa
import base64

app = FastAPI()
blockchain = Blockchain()
openchain = OpenChain(nodes=[])
token_pool = TokenPool()

new_block = False

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Wallet(BaseModel):
    wallet_name: str
    private_key: str
    public_key: str


@app.get('/api/mine_block')
async def mine_block():
    """
    Mine the oldest block in the openchain
    Returns message if the block was mined successfully
    """
    # Get last open transaction
    last_transaction = openchain.get_last_open_block()
    if last_transaction is None:
        return {'message': 'No open blocks to mine'}
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof=previous_proof)
    previous_hash = blockchain.hash_block(block=previous_block)

    block = blockchain.create_block(proof=proof, previous_hash=previous_hash, origin=last_transaction['origin'], amount=
    last_transaction['amount'], signature=last_transaction['signature'], destination=last_transaction['destination'])
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
        'chain': blockchain.chain,
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
    if block.amount == '':
        return {'message', 'Cannot create block with empty resource'}
    #if blockchain.verify_ownership(pub_key=block.origin, signature=block.signature, amount=block.amount):
    openchain.create_block(origin=block.origin, amount=token_pool.get_amount(float(block.amount)),
                           signature=block.signature, destination=block.destination)
    return {'message': 'New block created on the openchain'}


@app.get('/api/get_openchain')
async def get_openchain():
    """
    Retrieve the current openchain with non verified blocks
    Returns the chain and it's current length
    """
    return {
        'chain': openchain.chain,
        'chain_length': len(openchain.chain)
    }


@app.get('/api/get_blocks')
async def get_blocks(wallet_address=''):
    """
    Get all blocks from blockchain for certain wallet address.
    Query Param: wallet_address: Wallet address of the block origin or destination
    Returns: List of blocks
    """
    blocks = []
    for block in blockchain.chain:
        if block['origin'] == wallet_address or block['destination'] == wallet_address:
            blocks.append(block)
    return blocks


@app.get('/api/verify_wallet')
async def verify_wallet(priv_key: str = '', pub_key: str = ''):
    """
    Verify wallet private and public key
    Query Param: priv_key: Private key of the wallet
                 pub_key: Public key of the wallet
    Returns: String "Wallet is verified" when wallet is legit
    """
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(priv_key), curve=ecdsa.SECP256k1)
    vk = ecdsa.VerifyingKey.from_string(base64.b64decode(pub_key), curve=ecdsa.SECP256k1)
    # Sign a dummy message for the verification process
    sig = sk.sign(b'message')
    try:
        # Verify the key pair, throws exception when keys don't match
        vk.verify(sig, b'message')
        return "Wallet is verified"
    except ecdsa.keys.BadSignatureError as e:
        return "Wallet not verified"


@app.get('/api/create_wallet')
async def create_wallet(wallet_name=''):
    """
    Create a new wallet to interact with the blockchain
    Query Param: wallet_name: Name of the wallet
    Returns: Wallet name, private and public key as JSON object
    """
    sk = SigningKey.generate(curve=SECP256k1)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    # Make it shorter and therefore more readable
    public_key = base64.b64encode(bytes.fromhex(public_key))
    wallet = Wallet(private_key=private_key, public_key=public_key, wallet_name=wallet_name)
    return wallet


@app.get('/api/get_wallet_balance')
async def get_wallet_balance(wallet_address: str = ''):
    my_blockchain = blockchain.chain
    balance = 0.0
    for block in my_blockchain:
        if block['destination'] == wallet_address:
            balance += float(block['amount'])
        if block['origin'] == wallet_address:
            balance -= float(block['amount'])
    return {"balance": balance}


@app.websocket('/ws/blockchain')
async def broadcast_blockchain(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(5)
        await websocket.send_json(blockchain.chain)


@app.websocket('/ws/openchain')
async def broadcast_openchain(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(5)
        await websocket.send_json(openchain.chain)