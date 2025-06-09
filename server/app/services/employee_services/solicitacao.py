from flask import session
from datetime import datetime, timezone
from app.database.db import SessionLocal
from app.models.solicitacao import SolicitacaoConta
from app.models.cliente import Cliente
from app.models.usuario import Usuario

def listar_solicitacoes_pendentes():
    if 'id_funcionario' not in session or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado. Apenas admins e gerentes podem ver solicitações.'}, 403

    db = SessionLocal()
    try:
        solicitacoes = (
            db.query(
            SolicitacaoConta.id_solicitacao,
            SolicitacaoConta.tipo_conta,
            SolicitacaoConta.valor_inicial,
            SolicitacaoConta.data_solicitacao,
            Usuario.nome.label("nome_cliente")
        )
        .join(Cliente, SolicitacaoConta.id_cliente == Cliente.id_cliente)
        .join(Usuario, Cliente.id_usuario == Usuario.id_usuario)
        .filter(SolicitacaoConta.status == 'PENDENTE')
        .all()
    )

        resultado = []
        for s in solicitacoes:
            resultado.append({
                'id_solicitacao': s.id_solicitacao,
                'tipo_conta': s.tipo_conta,
                'valor_inicial': float(s.valor_inicial or 0),
                'data_solicitacao': s.data_solicitacao.isoformat(),
                'nome_cliente': s.nome_cliente
            })

        return resultado, 200
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()

def aprovar_solicitacao(id_solicitacao, id_funcionario):
    if 'id_funcionario' not in session or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado. Apenas admins e gerentes podem aprovar solicitações.'}, 403

    db = SessionLocal()
    try:
        solicitacao = db.query(SolicitacaoConta).get(id_solicitacao)
        if not solicitacao:
            return {'erro': 'Solicitação não encontrada'}, 404

        if solicitacao.status != 'PENDENTE':
            return {'erro': 'Solicitação já foi processada.'}, 400

        solicitacao.status = 'APROVADO'
        solicitacao.id_funcionario_aprovador = id_funcionario
        solicitacao.data_aprovacao = datetime.now(timezone.utc)

        db.commit()
        return {'mensagem': 'Solicitação aprovada com sucesso.'}, 200
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()

def rejeitar_solicitacao(id_solicitacao, id_funcionario):
    if 'id_funcionario' not in session or session.get('cargo') not in ['Admin', 'Gerente']:
        return {'erro': 'Acesso negado. Apenas admins e gerentes podem rejeitar solicitações.'}, 403

    db = SessionLocal()
    try:
        solicitacao = db.query(SolicitacaoConta).get(id_solicitacao)
        if not solicitacao:
            return {'erro': 'Solicitação não encontrada'}, 404

        if solicitacao.status != 'PENDENTE':
            return {'erro': 'Solicitação já foi processada.'}, 400

        solicitacao.status = 'REJEITADO'
        solicitacao.id_funcionario_aprovador = id_funcionario
        solicitacao.data_aprovacao = datetime.now(timezone.utc)

        db.commit()
        return {'mensagem': 'Solicitação rejeitada com sucesso.'}, 200
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()
