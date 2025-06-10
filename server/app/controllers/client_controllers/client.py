from app.services.client_services.solicitacao import (
    solicitar_abertura_conta,
    verificar_possui_conta
)

def cliente_solicitar_abertura_conta(id_usuario, data):
    try:
        resultado = solicitar_abertura_conta(id_usuario, data)
        return resultado, 201
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500

def cliente_verificar_possui_conta(id_usuario):
    try:
        resultado = verificar_possui_conta(id_usuario)
        return resultado, 200
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
