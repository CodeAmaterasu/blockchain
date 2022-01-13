# Blockchain - M150
Project to show how a blockchain works, the crypto currency "DPT - Deep Fried Token" runs on it.

## Technologies used

The project is written in python 3.9 using Docker container as deployment solution.

For CD we use Jenkins.

## Project Structure

File | Description
:--- |:--- |
main.py | This file contains all the API logic for FastAPI. More information on the API: https://blockchain.danilojakob.ch/docs
blockchain.py | This file contains all the logic for the blockchain. Verifying the blockchain, verifying the ownership of a new block and mining.
openchain.py | This file contains the logic for the OpenChain, a list of Blocks which are not verified yet (mined). Every block which is created on the blockchain, first goes into the OpenChain before being appenden into the blockchain.
token.py | This file contains the Token class, this class holds all available tokens (functions like a bank). Every participant in the blockchain can withdraw from that pool of tokens.

## Documentation

The complete code is documented using pydoc, so for detailed information about the functionality please refer to the code.

You can access a detailed API Documentation provided by FastAPI using following link: https://blockchain.danilojakob.ch/docs

## Running as Docker container

Install docker and docker-compose for the respective OS.

Execute following command:
```shell
docker-compose up --build
```
Now you can access the API at ``http://localhost:10000`` and the api docs at ``http://localhsot:10000/docs``
