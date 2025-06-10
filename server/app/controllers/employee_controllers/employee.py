from flask import session
from app.services.employee_services.solicitacao import (
    listar_solicitacoes_pendentes,
    aprovar_solicitacao,
    rejeitar_solicitacao
)

def employee_listar_solicitacoes_pendentes():
    if not session.get('id_funcionario') or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado.'}, 403

    try:
        resultado = listar_solicitacoes_pendentes()
        return resultado, 200
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_aprovar_solicitacao(id_solicitacao, id_funcionario):
    if not session.get('id_funcionario') or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado.'}, 403

    try:
        resultado = aprovar_solicitacao(id_solicitacao, id_funcionario)
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 400
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_rejeitar_solicitacao(id_solicitacao, id_funcionario):
    if not session.get('id_funcionario') or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado.'}, 403

    try:
        resultado = rejeitar_solicitacao(id_solicitacao, id_funcionario)
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 400
    except Exception as e:
        return {'erro': str(e)}, 500
