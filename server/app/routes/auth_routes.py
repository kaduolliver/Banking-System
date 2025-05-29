from flask import Blueprint, request
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
