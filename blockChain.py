import hashlib
import json
from textwrap import dedent
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain  = []
        self.nodes = set()
    
        #Creating the Genesis Block which is the first Block and has no predecessors
        self.new_block(previous_hash=1, proof=100)
    
    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
        
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <str> A blockchain
        :return: <bool> True if valid, False if not
        """
        
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            #Checking the has of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            #Checking that is the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
        
        return True
    
    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """
        
        neighbours = self.nodes
        new_chain = None
        
        #We are only looking for chains longer than ours
        max_length = len(self.chain)
        
        #Grabbing and verifying the chains from all the nodes in our network for node in neighbours:
        for node in neighbours:
            response = requests.get(f'http://{node}/return_chain')
            
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                #checking if the length if longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
                    
        #Replacing our chain if we discover a new and valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False
    
    #Creating a new block and adding it to the chain    
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work Algorithm
        :param previous_hash: (Optional) <str> The hash of the previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) +1,
            'timestamp':time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])            
            }
        
        #Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    #Creates a new transaction and adds it to the list above
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        
        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1
     
    #Returns the last Block in the chain
    @property
    def last_block(self):
        return self.chain[-1] 
        
    #Hashing of a Block
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
    
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        1. Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
        2. p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
#Instantiate the Node
app = Flask(__name__)

#Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Blockchain
blockchain = Blockchain()