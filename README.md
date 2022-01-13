# Blockchain
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


## Disclaimer

This project should give a pretty good idea of how a simple blockchain works. But keep in mind it's still a simple blockchain.

With that in mind don't try to use this repository as basis for a Blockchain running in a production environment, because full-fledged security wasn't the top priority.

## License

This repository and the other affiliated repositories, namely [blockchain-explorer](https://github.com/CodeAmaterasu/blockchain-explorer) and [blockchain-client](https://github.com/CodeAmaterasu/blockchain-client) are licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

This means you can change the code, distribute it or sell it for commercial use.
