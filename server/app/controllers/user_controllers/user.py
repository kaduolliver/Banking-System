from app.services.user_services.userData import (
    add_endereco,
    get_endereco,
    atualizar_usuario
)

def user_add_endereco(data):
    try:
        resultado = add_endereco(data)
        return resultado, 200
    except Exception as e:
        return {"erro": str(e)}, 500

def user_get_endereco():
    try:
        resultado = get_endereco()
        return resultado, 200
    except Exception as e:
        return {"erro": str(e)}, 500

def user_atualizar_usuario(data):
    try:
        resultado = atualizar_usuario(data)
        return resultado, 200
    except Exception as e:
        return {"erro": str(e)}, 500
