from flask import Blueprint, jsonify, session
from app.controllers.employee_controllers.employee import (
    employee_listar_solicitacoes_pendentes,
    employee_aprovar_solicitacao,
    employee_rejeitar_solicitacao
)
from app.controllers.employee_controllers.employee import (
    employee_listar_funcionarios,
    employee_atualizar_status
)
from app.controllers.employee_controllers.employee import (
    employee_listar_emprestimos_pendentes,
    employee_decidir_emprestimo
)

employee_bp = Blueprint('funcionario', __name__)


# Solicitações de crição de contas
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

#----------------------------------------------------------------------------------------


# Painel de controle de funcionários (ADM)
@employee_bp.route('/api/employees', methods=['GET'])
def route_listar_funcionarios():
    funcionario_id = session.get('id_funcionario')
    cargo = session.get('cargo')

    if not funcionario_id or cargo not in ['Admin']:
        return jsonify({'erro': 'Funcionário não autenticado ou sem permissão'}), 401

    resposta, status = employee_listar_funcionarios()
    return jsonify(resposta), status

@employee_bp.route('/api/<int:id_funcionario>/status', methods=['PUT'])
def route_atualizar_status(id_funcionario):
    funcionario_id = session.get('id_funcionario')
    cargo = session.get('cargo')

    if not funcionario_id or cargo not in ['Admin']:
        return jsonify({'erro': 'Funcionário não autenticado ou sem permissão'}), 401

    resposta, status = employee_atualizar_status(id_funcionario)
    return jsonify(resposta), status
#----------------------------------------------------------------------------------------


# Solicitações de empréstimos manuais
@employee_bp.route('/api/emprestimos/pendentes', methods=['GET'])
def route_listar_emprestimos_pendentes():
    if not session.get('id_funcionario'):
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = employee_listar_emprestimos_pendentes()
    return jsonify(resposta), status

@employee_bp.route('/api/emprestimos/<int:id_emprestimo>/decidir', methods=['PUT'])
def route_decidir_emprestimo(id_emprestimo):
    funcionario_id = session.get('id_funcionario')
    if not funcionario_id:
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = employee_decidir_emprestimo(id_emprestimo, funcionario_id)
    return jsonify(resposta), status

#----------------------------------------------------------------------------------------