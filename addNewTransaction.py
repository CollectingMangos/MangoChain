from flask import jsonify, request
from blockChain import app, blockchain

@app.route('/add_new_transaction', methods=['POST'])
def add_new_transaction():
    values = request.get_json()
    
    #Check that the required fields are in the POST'ed data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing required values', 400
    
    #Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message': f'Transaction will be added to the Block {index}'}
    return jsonify(response), 201

@app.route('/return_chain', methods=['GET'])
def return_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200