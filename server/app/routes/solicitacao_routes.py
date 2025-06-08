from flask import Blueprint, request, jsonify, session
from app.controllers.solicitacao_controller import solicitar_abertura_conta, verificar_possui_conta, aprovar_solicitacao

solicitacao_bp = Blueprint('solicitacoes', __name__)

@solicitacao_bp.route('/api/solicitacoes', methods=['POST'])
def route_solicitar_abertura():
    resposta, status = solicitar_abertura_conta(request.json)
    return jsonify(resposta), status

@solicitacao_bp.route('/api/cliente/<int:cliente_id>/conta', methods=['GET'])
def route_verificar_conta(cliente_id):
    resposta, status = verificar_possui_conta(cliente_id)
    return jsonify(resposta), status

@solicitacao_bp.route('/api/solicitacoes/<int:id_solicitacao>/aprovar', methods=['POST'])
def route_aprovar_solicitacao(id_solicitacao):
    if 'id_usuario' not in session or session.get('cargo') != 'gerente':
        return jsonify({'erro': 'Acesso negado. Apenas gerentes podem aprovar solicitações.'}), 403

    funcionario_id = session.get('id_funcionario') 
    resposta, status = aprovar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status