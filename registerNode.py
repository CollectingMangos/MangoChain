from flask import jsonify, request
from blockChain import app, blockchain

@app.route('/register_node', methods=['POST'])
def register_nodes():    
    values = request.get_json()
    
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)
        
    response = {
        'message': 'New nodes have been successfully added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201