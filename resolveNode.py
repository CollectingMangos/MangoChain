from flask import jsonify, request
from blockChain import app, blockchain

@app.route('/resolve_node', methods=['GET'])
def consensus():
        replaced = blockchain.resolve_conflicts()
        
        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is the OG',
                'chain': blockchain.chain
            }
        return jsonify(response), 200