from app.services.agency_services.agency import (
    listar_agencias, 
    add_endereco_agencia, 
    get_endereco_agencia,
    update_endereco_agencia 
)

def agency_listar_agencias():
    try:
        agencias_data = listar_agencias()
        return agencias_data, 200
    except Exception as e:
        return {"erro": str(e)}, 500

def agency_add_endereco_agencia(agencia_id, data):
    try:
        resultado = add_endereco_agencia(agencia_id, data) 
        return resultado, 201
    except Exception as e:
        return {"erro": str(e)}, 500

def agency_update_endereco_agencia(agencia_id, data):
    try:
        resultado = update_endereco_agencia(agencia_id, data)
        return resultado, 200 
    except Exception as e:
        return {"erro": str(e)}, 500

def agency_get_endereco_agencia(agencia_id):
    try:
        endereco = get_endereco_agencia(agencia_id)
        return endereco, 200
    except Exception as e:
        return {"erro": str(e)}, 500
    