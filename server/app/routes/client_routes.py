from flask import Blueprint, request, jsonify
from app.controllers.client_controller import add_endereco, get_endereco

client_bp = Blueprint('cliente', __name__)

@client_bp.route('/api/cliente/endereco', methods=['POST', 'PUT'])
def endereco_route():
    resposta, status = add_endereco(request.json)
    return jsonify(resposta), status

@client_bp.route('/api/cliente/endereco', methods=['GET'])
def endereco_get_route():
    resposta, status = get_endereco()
    return jsonify(resposta), status













