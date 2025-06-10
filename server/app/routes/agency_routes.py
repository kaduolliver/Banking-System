from flask import Blueprint, request, jsonify
from app.controllers.agency_controllers.agency import (
    agency_listar_agencias,
    agency_add_endereco_agencia,
    agency_get_endereco_agencia
)

agency_bp = Blueprint('agencia', __name__)

@agency_bp.route('/api/agencias', methods=['GET'])
def get_agencias_route():
    resposta, status = agency_listar_agencias()
    return jsonify(resposta), status

@agency_bp.route('/api/agencia/endereco', methods=['POST'])
def salvar_endereco_agencia():
    data = request.get_json()
    resposta, status = agency_add_endereco_agencia(data)
    return jsonify(resposta), status

@agency_bp.route('/api/agencia/endereco', methods=['GET'])
def obter_endereco_agencia():
    id_agencia = request.args.get('id')
    resposta, status = agency_get_endereco_agencia(id_agencia)
    return jsonify(resposta), status
