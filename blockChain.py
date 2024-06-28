import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class blockChain(object):
    def __init__(self):
        self.chain  = []
        self.currentTransactions = []
    
    #Creating the Genesis Block which is the first Block and has no predessessors
        self.newBlock(previousHash=1, proof=100)
    
    
    #Creating a new block and adding it to the chain    
    def newBlock(self, proof, previousHash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work Algorithm
        :param previousHash: (Optional) <str> The has of the previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) +1,
            'timestamp':time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previousHash': previousHash or self.hash(self.chain[-1])            
            }
        
        #Reser the current list of transactions
        self.currentTransactions = []
        self.chain.append(block)
        return block
    
    #Creates a new transaction and adds it to the list above
    def newTransaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        
        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.lastBlock['index'] + 1
     
    #Returns the last Block in the chain
    @property
    def lastBlock(self):
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
    