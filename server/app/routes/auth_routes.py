from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import registrar_usuario, login_usuario, validar_otp, verificar_sessao

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register_route():
    resposta, status = registrar_usuario(request.json)
    return jsonify(resposta), status

@auth_bp.route('/api/login', methods=['POST'])
def login_route():
    resposta, status = login_usuario(request.json)
    return jsonify(resposta), status

@auth_bp.route('/api/validar-otp', methods=['POST'])
def validar_otp_route():
    resposta, status = validar_otp(request.json)
    return jsonify(resposta), status

@auth_bp.route('/api/sessao', methods=['GET'])
def verificar_sessao_route():
    resposta, status = verificar_sessao()
    return jsonify(resposta), status

@auth_bp.route('/api/logout', methods=['POST'])
def logout_route():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso.'}), 200
