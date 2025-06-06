from flask import Blueprint, request, jsonify
from app.controllers.user_controller import atualizar_usuario

user_bp = Blueprint('usuario', __name__)

@user_bp.route('/api/usuario/atualizar', methods=['PUT'])
def atualizar_usuario_route():
    resposta, status = atualizar_usuario(request.json)
    return jsonify(resposta), status


