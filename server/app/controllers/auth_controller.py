from flask import session
from app.services.auth_services import (
    registrar_usuario,
    login_usuario,
    validar_otp,
    verificar_sessao
)
from app.services.auth_services import obter_usuario_atual

def auth_registrar_usuario(data):
    try:
        return registrar_usuario(data)
    except Exception as e:
        return {"erro": str(e)}, 500

def auth_login_usuario(data):
    try:
        return login_usuario(data)
    except Exception as e:
        return {"erro": str(e)}, 500

def auth_validar_otp(data):
    try:
        return validar_otp(data)
    except Exception as e:
        return {"erro": str(e)}, 500

def auth_verificar_sessao():
    try:
        return verificar_sessao()
    except Exception as e:
        return {"erro": str(e)}, 500

def user_get_profile():
    if 'id_usuario' not in session:
        return {'erro': 'Não autenticado'}, 401
    try:
        dados = obter_usuario_atual(session['id_usuario'])
        return dados, 200
    except LookupError as e:
        return {'erro': str(e)}, 404
    except Exception as e:
        return {'erro': str(e)}, 500