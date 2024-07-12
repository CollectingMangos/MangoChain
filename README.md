# MangoChain AKA [Blockchain] in Python

This project implements a simple blockchain and a basic API to interact with it. The blockchain includes functionalities for mining new blocks, creating new transactions, and achieving consensus among nodes.

## Features

- **Genesis Block Creation:** The first block, known as the genesis block, is created with a predefined proof and previous hash.
- **Transaction Management:** Add new transactions that will be recorded in the next mined block.
- **Mining:** Implement a simple proof-of-work algorithm to mine new blocks and add them to the blockchain.
- **Node Registration:** Nodes can be registered to the network.
- **Consensus Algorithm:** Implement a basic consensus algorithm to resolve conflicts by ensuring the longest valid chain is adopted.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/CollectingMangos/MangoChain.git
    cd MangoChain
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the MangoChain application, run the `main.py` file:

```sh
python main.py
```

The application will start running on `http://0.0.0.0:9000`.

## API Endpoints

### Mine a new block

- **URL:** `/mine_block`
- **Method:** `GET`
- **Description:** Mines a new block and adds it to the Mangochain.

### Create a new transaction

- **URL:** `/add_new_transaction`
- **Method:** `POST`
- **Description:** Adds a new transaction to the next mined block.
- **Request Body:**

    ```json
    {
        "sender": "address_of_sender",
        "recipient": "address_of_recipient",
        "amount": {int}
    }
    ```

### Get the entire blockchain

- **URL:** `/return_chain`
- **Method:** `GET`
- **Description:** Returns the current state of the Mangochain.

### Register new nodes

- **URL:** `/register_node`
- **Method:** `POST`
- **Description:** Registers a new node to the network.
- **Request Body:**

    ```json
    {
        "nodes": ["http://192.168.0.5:5000", "http://192.168.0.6:5000"]
    }
    ```

### Resolve conflicts

- **URL:** `/resolve_node`
- **Method:** `GET`
- **Description:** Resolves conflicts by replacing the chain with the longest one in the network.

## Code Structure

- `main.py`: The main entry point for running the application.
- `blockchain.py`: Contains the main logic for the Mangochain including block creation, transaction management, mining, and consensus algorithm.
- `mineBlock.py`: Handles the endpoint for mining new blocks.
- `addNewTransaction.py`: Handles the endpoint for adding new transactions.
- `registerNode.py`: Handles the endpoint for registering new nodes.
- `resolveNode.py`: Handles the endpoint for resolving conflicts.
- `exampleOfBlock.txt`: An example of a block structure.
- `requirements.txt`: Contains the project dependencies.

## Dependencies

- **Flask:** A micro web framework for Python.
- **Requests:** A simple HTTP library for Python.
- **Hashlib:** A library for hashing in Python.
- **Json:** A library for handling JSON data.
- **UUID:** A library for generating unique identifiers.
- **Urllib:** A library for URL parsing.

## License

This project is licensed under the MIT License.
