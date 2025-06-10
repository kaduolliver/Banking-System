from app.services.auth_services import (
    registrar_usuario,
    login_usuario,
    validar_otp,
    verificar_sessao
)

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
