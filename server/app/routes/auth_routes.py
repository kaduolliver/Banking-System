from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import registrar_usuario, login_usuario, validar_otp

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    return registrar_usuario(request.json)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    return login_usuario(request.json)

@auth_bp.route('/api/validar-otp', methods=['POST'])
def validar_otp_route():
    return validar_otp(request.json)

@auth_bp.route('/api/sessao', methods=['GET'])
def verificar_sessao():
    if 'id_usuario' in session:
        return jsonify({'autenticado': True, 'id_usuario': session['id_usuario'], 'tipo_usuario': session['tipo']}), 200
    else:
        return jsonify({'autenticado': False}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso.'}), 200

