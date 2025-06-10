from app.services.user_services.userData import (
    add_endereco,
    get_endereco,
    atualizar_usuario
)

def user_add_endereco(data):
    try:
        resultado, status = add_endereco(data)
        return resultado, status
    except Exception as e:
        return {"erro": str(e)}, 500


def user_get_endereco():
    try:
        resultado, status = get_endereco()
        return resultado, status
    except Exception as e:
        return {"erro": str(e)}, 500

def user_atualizar_usuario(data):
    try:
        resultado, status = atualizar_usuario(data)
        return resultado, status
    except Exception as e:
        return {"erro": str(e)}, 500
