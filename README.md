# Blockchain - M150
Project to show how a blockchain works

## What is a blockchain and how does it work?

In simple terms a blockchain is a shared and immutable ledger in which transactions and assets can be tracked within the network.
<br>
<br>
Those assets can be money (e.g. Cryptocurrencies), estates, patents, digital licenses (e.g. NFT) etc.
<br>
In this sense virtually anything of value can be tracked and traded on a blockchain. But how does it work?
<br>
<br>
The first and most important thing to know about a blockchain is, that it's decentralized. This means that the blockchain is not "stored" on a single server or node.
<br>
A blockchain runs on lots of different computers and servers and is therefore more secure against a data breach because an attacker couldn't possibly steal or manipulate all the data.

![Blockchain-explained](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fintellipaat.com%2FmediaFiles%2F2019%2F02%2FBlockchain-05.jpg&f=1&nofb=1)
<br>
<br>
This images shows how the blockchain works, the first step is a user requesting a transaction (making a transaction). A non verified block is now being created.
<br>
The block is then broadcasted to all nodes in the blockchain network. The nodes then validate the transaction / block.
<br>
This procedure is called mining, after the block is mined by a node, the miner receives a reward for the computational work in form of a transaction fee.
<br>
After the block is verified it is being appended to the current blockchain and the process is therefore finished.

## Running as Docker container

Install docker and docker-compose for the respective OS.

Execute following command:
```shell
docker-compose up --build
```
Now you can access the API at ``http://localhost:8080`` and the api docs at ``http://localhsot:8080/docs``
