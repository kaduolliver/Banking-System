from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import registrar_usuario, login_usuario, validar_otp
from app.database.db import SessionLocal
from app.models.usuario import Usuario

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
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(id_usuario=session['id_usuario']).first()
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404

            return jsonify({
                'autenticado': True,
                'id_usuario': usuario.id_usuario,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'telefone': usuario.telefone,
                'tipo_usuario': usuario.tipo_usuario
            }), 200
        finally:
            db.close()
    else:
        return jsonify({'autenticado': False}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso.'}), 200
