from flask import Blueprint, request, jsonify
from app.controllers.client_controllers.client import solicitar_abertura_conta, verificar_possui_conta

client_bp = Blueprint('client', __name__)

@client_bp.route('/api/solicitacoes', methods=['POST'])
def route_solicitar_abertura():
    resposta, status = solicitar_abertura_conta(request.json)
    return jsonify(resposta), status

@client_bp.route('/api/cliente/<int:cliente_id>/conta', methods=['GET'])
def route_verificar_conta(cliente_id):
    resposta, status = verificar_possui_conta(cliente_id)
    return jsonify(resposta), status







