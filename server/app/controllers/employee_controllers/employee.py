from app.services.employee_services.solicitacao import listar_solicitacoes_pendentes, aprovar_solicitacao, rejeitar_solicitacao
from app.services.employee_services.agency import add_endereco_agencia, get_endereco_agencia

# Solicitações

def employee_listar_solicitacoes_pendentes():
    return listar_solicitacoes_pendentes()

def employee_aprovar_solicitacao_service(id_solicitacao, id_funcionario):
    return aprovar_solicitacao(id_solicitacao, id_funcionario)

def employee_rejeitar_solicitacao_service(id_solicitacao, id_funcionario):
    return rejeitar_solicitacao(id_solicitacao, id_funcionario)

# Agência

def employee_add_endereco_agencia(data):
    return add_endereco_agencia(data)

def employee_get_engereco_agencia(id_agencia):
    return get_endereco_agencia(id_agencia)