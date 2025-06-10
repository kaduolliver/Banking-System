from flask import Blueprint, jsonify, session
from app.controllers.employee_controllers.employee import (
    employee_listar_solicitacoes_pendentes,
    employee_aprovar_solicitacao,
    employee_rejeitar_solicitacao
)

employee_bp = Blueprint('funcionario', __name__)

@employee_bp.route('/api/solicitacoes/pendentes', methods=['GET'])
def route_listar_solicitacoes_pendentes():
    funcionario_id = session.get('id_funcionario')

    if not funcionario_id:
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = employee_listar_solicitacoes_pendentes()
    return jsonify(resposta), status

@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/aprovar', methods=['POST'])
def route_aprovar_solicitacao(id_solicitacao):
    funcionario_id = session.get('id_funcionario')

    if not funcionario_id:
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = employee_aprovar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status

@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/rejeitar', methods=['POST'])
def route_rejeitar_solicitacao(id_solicitacao):
    funcionario_id = session.get('id_funcionario')

    if not funcionario_id:
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = employee_rejeitar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status
