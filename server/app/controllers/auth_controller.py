from app.services.auth_services import (
    registrar_usuario as registrar_usuario_service,
    login_usuario as login_usuario_service,
    validar_otp as validar_otp_service,
    verificar_sessao as verificar_sessao_service
)

def registrar_usuario(data):
    return registrar_usuario_service(data)

def login_usuario(data):
    return login_usuario_service(data)

def validar_otp(data):
    return validar_otp_service(data)

def verificar_sessao():
    return verificar_sessao_service()
