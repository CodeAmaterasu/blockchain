# Blockchain - M150
Project to show how a blockchain works, the crypto currency "DPT - Deep Fried Token" runs on it.

## Technologies used

The project is written in python 3.9 using Docker container as deployment solution.

For CD we use Jenkins.

## Project Structure

![Project Structure](docs/assets/project_structure.png)

## Running as Docker container

Install docker and docker-compose for the respective OS.

Execute following command:
```shell
docker-compose up --build
```
Now you can access the API at ``http://localhost:10000`` and the api docs at ``http://localhsot:10000/docs``
