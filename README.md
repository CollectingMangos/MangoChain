# MangoChain AKA [Blockchain] in Python

This project implements a simple blockchain and a basic API to interact with it. The blockchain includes functionalities for mining new blocks, creating new transactions, and achieving consensus among nodes.

## Features

1. **Genesis Block Creation**: The first block, known as the genesis block, is created with a predefined proof and previous hash.
2. **Transaction Management**: Add new transactions that will be recorded in the next mined block.
3. **Mining**: Implement a simple proof-of-work algorithm to mine new blocks and add them to the blockchain.
4. **Node Registration**: Nodes can be registered to the network.
5. **Consensus Algorithm**: Implement a basic consensus algorithm to resolve conflicts by ensuring the longest valid chain is adopted.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/CollectingMangos/MangoChain.git
    cd your_repo_name
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```bash
    python3 blockchain.py
    ```

2. **API Endpoints**:
    - **Mine a new block**:
        ```http
        GET /mine_block
        ```
    - **Create a new transaction**:
        ```http
        POST /add_new_transaction
        {
            "sender": "address_of_sender",
            "recipient": "address_of_recipient",
            "amount": 5
        }
        ```
    - **Get the entire blockchain**:
        ```http
        GET /return_chain
        ```
    - **Register new nodes**:
        ```http
        POST /register_node
        {
            "nodes": ["http://192.168.0.5:5000", "http://192.168.0.6:5000"]
        }
        ```
    - **Resolve conflicts**:
        ```http
        GET /resolve_node
        ```

## Code Structure

- **blockchain.py**: Contains the main logic for the blockchain including block creation, transaction management, mining, and consensus algorithm.

## Dependencies

- **Flask**: A micro web framework for Python.
- **Requests**: A simple HTTP library for Python.
- **Hashlib**: A library for hashing in Python.
- **Json**: A library for handling JSON data.
- **UUID**: A library for generating unique identifiers.
- **Urllib**: A library for URL parsing.

## License

This project is licensed under the MIT License.

---
