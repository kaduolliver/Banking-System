from flask import Blueprint, request, jsonify
from app.controllers.user_controllers.user import (
    user_atualizar_usuario,
    user_add_endereco,
    user_get_endereco
)

user_bp = Blueprint('usuario', __name__)

@user_bp.route('/api/usuario/atualizar', methods=['PUT'])
def atualizar_usuario_route():
    resposta, status = user_atualizar_usuario(request.json)
    return jsonify(resposta), status

@user_bp.route('/api/usuario/endereco', methods=['POST', 'PUT'])
def endereco_route():
    resposta, status = user_add_endereco(request.json)
    return jsonify(resposta), status

@user_bp.route('/api/usuario/endereco', methods=['GET'])
def endereco_get_route():
    resposta, status = user_get_endereco()
    return jsonify(resposta), status
