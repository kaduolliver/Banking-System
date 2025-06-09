from flask import Blueprint, jsonify, session, request
from app.controllers.employee_controllers.employee import aprovar_solicitacao, rejeitar_solicitacao, listar_solicitacoes_pendentes
from app.services.employee_services.agency import add_endereco_agencia, get_endereco_agencia

employee_bp = Blueprint('funcionario', __name__)

@employee_bp.route('/api/solicitacoes/pendentes', methods=['GET'])
def route_listar_solicitacoes_pendentes():
    funcionario_id = session.get('id_funcionario')

    if not funcionario_id:
        return jsonify({'erro': 'Funcionário não autenticado'}), 401

    resposta, status = listar_solicitacoes_pendentes()
    return jsonify(resposta), status


@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/aprovar', methods=['POST'])
def route_aprovar_solicitacao(id_solicitacao):

    funcionario_id = session.get('id_funcionario')
    resposta, status = aprovar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status


@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/rejeitar', methods=['POST'])
def route_rejeitar_solicitacao(id_solicitacao):

    funcionario_id = session.get('id_funcionario')
    resposta, status = rejeitar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status


@employee_bp.route('/api/agencia/endereco', methods=['POST'])
def salvar_endereco_agencia():
    data = request.get_json()
    return add_endereco_agencia(data)

@employee_bp.route('/api/agencia/endereco', methods=['GET'])
def obter_endereco_agencia():
    id_agencia = request.args.get('id')
    return get_endereco_agencia(id_agencia)
