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
    
        #Creating the Genesis MangBlock which is the first Block and has no predecessors
        self.new_block(previous_hash=1, proof=100)
    
    def register_node(self, address):
        #Add a new node to the list of nodes

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
        
    def valid_chain(self, chain):
        #Determine if a given blockchain is valid
                
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            #Checking if the hash of the block is correct
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
    
    #Creating a new Mangblock and adding it to the chain    
    def new_block(self, proof, previous_hash=None):
        #Create a new MangBlock in the Blockchain
        
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
     
    #Returns the last MangBlock in the chain
    @property
    def last_block(self):
        return self.chain[-1] 
        
    #Hashing of a MangBlock, it creates a SHA-256 hash of a Block
    @staticmethod
    def hash(block):
        
        # We must make sure that the Dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        1. Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
        2. p is the previous proof, and p' is the new proof
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        #Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
#Instantiate the Node
app = Flask(__name__)

#Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Mango Blockchain!
blockchain = Blockchain()