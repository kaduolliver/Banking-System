from flask import Blueprint, request, jsonify
from app.controllers.cliente_controller import verificar_se_tem_conta, solicitar_abertura_conta

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/api/cliente/verificar-conta/<int:id_usuario>', methods=['GET'])
def rota_verificar_conta(id_usuario):
    return verificar_se_tem_conta(id_usuario)


@cliente_bp.route('/api/cliente/solicitar-conta', methods=['POST'])
def rota_solicitar_conta():
    data = request.get_json()
    id_usuario = data.get('id_usuario')

    if not id_usuario:
        return jsonify({'erro': 'ID do usuário é obrigatório.'}), 400

    return solicitar_abertura_conta(id_usuario)
