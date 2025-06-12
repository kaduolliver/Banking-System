from flask import session, request
from app.services.employee_services.adm_config import listar_funcionarios, atualizar_status_funcionario
from app.services.employee_services.solicitacao import (
    listar_solicitacoes_pendentes,
    aprovar_solicitacao,
    rejeitar_solicitacao
)

def employee_listar_solicitacoes_pendentes():
    # if not session.get('id_funcionario') or session.get('cargo') not in ['Admin', 'Gerente']:
    #     return {'erro': 'Acesso negado.'}, 403

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

def employee_listar_funcionarios():
    if not session.get('id_funcionario') or session.get('cargo') not in ['Admin']:
        return {'erro': 'Acesso negado.'}, 403

    try:
        funcionarios = listar_funcionarios()
        return funcionarios, 200
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_atualizar_status(id_funcionario):
    if not session.get('id_funcionario') or session.get('cargo') not in ['Admin']:
        return {'erro': 'Acesso negado.'}, 403

    dados = request.get_json()
    if dados is None or 'inativo' not in dados:
        return {'erro': 'Campo "inativo" é obrigatório.'}, 400

    try:
        resultado = atualizar_status_funcionario(id_funcionario, dados['inativo'])
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 404
    except Exception as e:
        return {'erro': str(e)}, 500
