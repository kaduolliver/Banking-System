from app.services.agency_services.agency import get_endereco_agencia
from app.models.conta import Conta
from app.models.contaCorrente import ContaCorrente
from app.models.contaInvestimento import ContaInvestimento
from app.models.contaPoupanca import ContaPoupanca

def montar_dados_usuario(usuario):
    cargo = None
    id_funcionario = None
    id_agencia = None
    nome_agencia = None
    codigo_agencia = None
    endereco = None
    status_endereco = None
    inativo = None
    contas = []

    if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
        funcionario = usuario.funcionario
        cargo = funcionario.cargo
        id_funcionario = funcionario.id_funcionario
        inativo = funcionario.inativo
        if funcionario.agencia:
            agencia = funcionario.agencia
            id_agencia = agencia.id_agencia
            nome_agencia = agencia.nome
            codigo_agencia = agencia.codigo_agencia
            endereco, status_endereco = get_endereco_agencia(id_agencia)

    elif usuario.tipo_usuario == 'cliente' and usuario.cliente:
        for conta in usuario.cliente.contas:
            dados_conta = {
                'id_conta': conta.id_conta,
                'numero_conta': conta.numero_conta,
                'agencia': conta.agencia.codigo_agencia if conta.agencia else None,
                'tipo': None,
                'saldo': float(conta.saldo), 
                'status': conta.status,
                'data_abertura': conta.data_abertura.isoformat() if conta.data_abertura else None,
                'dados_especificos': {}
            }

            if conta.corrente:
                cc = conta.corrente
                dados_conta['tipo'] = 'corrente'
                dados_conta['dados_especificos'] = {
                    'limite': cc.limite,
                    'data_vencimento': cc.data_vencimento.isoformat() if cc.data_vencimento else None,
                    'taxa_manutencao': cc.taxa_manutencao
                }

            elif conta.poupanca:
                cp = conta.poupanca
                dados_conta['tipo'] = 'poupanca'
                dados_conta['dados_especificos'] = {
                    'taxa_rendimento': cp.taxa_rendimento,
                    'ultimo_rendimento': cp.ultimo_rendimento
                }

            elif conta.investimento:
                ci = conta.investimento
                dados_conta['tipo'] = 'investimento'
                dados_conta['dados_especificos'] = {
                    'perfil_risco': ci.perfil_risco,
                    'valor_minimo': ci.valor_minimo,
                    'taxa_rendimento_base': ci.taxa_rendimento_base
                }

            contas.append(dados_conta)

        solicitacoes = []
        for s in usuario.cliente.solicitacoes_conta:
            solicitacoes.append({
                'id_solicitacao': s.id_solicitacao,
                'tipo_conta': s.tipo_conta,
                'data_solicitacao': s.data_solicitacao.isoformat(),
                'status': s.status,
                'observacoes': s.observacoes,
                'valor_inicial': float(s.valor_inicial),
                'data_aprovacao': s.data_aprovacao.isoformat() if s.data_aprovacao else None
            })
    else:
        solicitacoes = None

    dados = {
        'id_usuario': usuario.id_usuario,
        'tipo_usuario': usuario.tipo_usuario,
        'nome': usuario.nome,
        'cpf': usuario.cpf,
        'data_nascimento': usuario.data_nascimento.isoformat(),
        'telefone': usuario.telefone,
        'cargo': cargo,
        'id_funcionario': id_funcionario,
        'status_funcionario': inativo,
        'id_agencia': id_agencia,
        'nome_agencia': nome_agencia,
        'codigo_agencia': codigo_agencia,
        'endereco_agencia': endereco if status_endereco == 200 else None,
        'contas': contas if contas else None,
        'solicitacoes_conta': solicitacoes if solicitacoes else None
    }

    return dados
