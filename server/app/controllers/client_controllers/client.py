from app.services.client_services.clientRequest import (
    solicitar_abertura_conta,
    verificar_possui_conta
)
from app.services.client_services.clientLoan import (
    solicitar_emprestimo
)
from app.services.client_services.withdraw import (
    realizar_saque, 
    saque_por_qr
)
from app.services.client_services.deposit import (
    realizar_deposito,
    deposito_por_qr,
)
from app.services.client_services.transfer import ( 
    realizar_transferencia
)
from app.services.client_services.statement import ( 
    obter_extrato_cliente,
    gerar_pdf_extrato
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

def cliente_solicitar_emprestimo(id_usuario, data):
    try:
        resultado = solicitar_emprestimo(id_usuario, data)
        return resultado, 201 
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500

def cliente_realizar_saque(id_usuario, data):
    try:
        resultado = realizar_saque(id_usuario, data)
        return resultado, 201
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500

def cliente_realizar_saque_por_qr(token_data):
    try:
        resultado = saque_por_qr(token_data)
        return resultado, 201
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
    
def cliente_realizar_deposito(id_usuario, data):
    try:
        resultado = realizar_deposito(id_usuario, data)
        return resultado, 201
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500

def cliente_realizar_deposito_por_qr(token_data):
    try:
        resultado = deposito_por_qr(token_data)
        return resultado, 201
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
    
def cliente_realizar_transferencia(id_usuario: int, data: dict):
    try:
        resultado = realizar_transferencia(id_usuario, data)
        return resultado, 201 
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
    
def cliente_obter_extrato(id_usuario: int, start_date: str = None, end_date: str = None, limit: int = 10):
    try:
        resultado = obter_extrato_cliente(id_usuario, start_date, end_date, limit)
        return resultado, 200
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500

def cliente_gerar_pdf_extrato(id_usuario: int, start_date: str = None, end_date: str = None, limit: int = 10):
    try:
        extrato_data, status_code = cliente_obter_extrato(id_usuario, start_date, end_date, limit)

        if status_code != 200:
            return extrato_data, status_code

        pdf_buffer = gerar_pdf_extrato(extrato_data, id_usuario)
        return pdf_buffer, 200 
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500