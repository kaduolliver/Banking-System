from flask import Blueprint, request, jsonify
from app.controllers.solicitacao_controller import solicitar_abertura_conta, verificar_possui_conta

solicitacao_bp = Blueprint('solicitacoes', __name__)

@solicitacao_bp.route('/api/solicitacoes', methods=['POST'])
def route_solicitar_abertura():
    resposta, status = solicitar_abertura_conta(request.json)
    return jsonify(resposta), status

@solicitacao_bp.route('/api/cliente/<int:cliente_id>/conta', methods=['GET'])
def route_verificar_conta(cliente_id):
    resposta, status = verificar_possui_conta(cliente_id)
    return jsonify(resposta), status
