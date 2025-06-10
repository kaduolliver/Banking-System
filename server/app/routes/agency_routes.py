from flask import Blueprint, request, jsonify
from app.controllers.agency_controllers.agency import (
    agency_listar_agencias,
    agency_add_endereco_agencia,
    agency_get_endereco_agencia,
    agency_update_endereco_agencia
)

agency_bp = Blueprint('agencia', __name__)

@agency_bp.route('/api/agencias', methods=['GET'])
def get_agencias_route():
    resposta, status = agency_listar_agencias()
    return jsonify(resposta), status

@agency_bp.route('/api/agencias/<int:agencia_id>/endereco', methods=['POST'])
def salvar_endereco_agencia_route(agencia_id):
    data = request.get_json()
   
    resposta, status = agency_add_endereco_agencia(agencia_id, data) 
    return jsonify(resposta), status

@agency_bp.route('/api/agencias/<int:agencia_id>/endereco', methods=['PUT'])
def atualizar_endereco_agencia_route(agencia_id): 
    data = request.get_json()
    
    resposta, status = agency_update_endereco_agencia(agencia_id, data)
    return jsonify(resposta), status

@agency_bp.route('/api/agencias/<int:agencia_id>/endereco', methods=['GET'])
def obter_endereco_agencia_route(agencia_id): 
   
    resposta, status = agency_get_endereco_agencia(agencia_id)
    return jsonify(resposta), status

