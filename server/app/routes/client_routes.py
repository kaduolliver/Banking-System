from flask import Blueprint, request, jsonify, session
from app.controllers.client_controllers.client import (
    cliente_solicitar_abertura_conta,
    cliente_verificar_possui_conta
)

client_bp = Blueprint('client', __name__)

@client_bp.route('/api/solicitacoes', methods=['POST'])
def route_solicitar_abertura():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    data = request.get_json()
    resposta, status = cliente_solicitar_abertura_conta(session['id_usuario'], data)
    return jsonify(resposta), status

@client_bp.route('/api/cliente/<int:cliente_id>/conta', methods=['GET'])
def route_verificar_conta(cliente_id):
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    resposta, status = cliente_verificar_possui_conta(session['id_usuario'])
    return jsonify(resposta), status

