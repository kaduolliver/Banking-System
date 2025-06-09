from flask import Blueprint, request, jsonify
from app.controllers.user_controllers.user import atualizar_usuario
from app.controllers.user_controllers.user import add_endereco, get_endereco

user_bp = Blueprint('usuario', __name__)

@user_bp.route('/api/usuario/atualizar', methods=['PUT'])
def atualizar_usuario_route():
    resposta, status = atualizar_usuario(request.json)
    return jsonify(resposta), status

@user_bp.route('/api/usuario/endereco', methods=['POST', 'PUT'])
def endereco_route():
    resposta, status = add_endereco(request.json)
    return jsonify(resposta), status

@user_bp.route('/api/usuario/endereco', methods=['GET'])
def endereco_get_route():
    resposta, status = get_endereco()
    return jsonify(resposta), status
