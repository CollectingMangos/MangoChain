from flask import jsonify, request
from blockChain import app, blockchain, node_identifier

@app.route('/mine_block', methods=['GET'])
def mine_block():
    #We run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    #We must receive a reward (aka a Mangcoin) for finding the proof
    #The sender is "0" to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    
    #Forge the new MangBlock by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': "New MangBlock Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],    
    }
    return jsonify(response), 200