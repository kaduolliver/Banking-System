from datetime import datetime, timezone
from app.database.db import SessionLocal
from app.models.solicitacao import SolicitacaoConta
from app.models.cliente import Cliente
from app.models.usuario import Usuario

def listar_solicitacoes_pendentes():
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

        return [{
            'id_solicitacao': s.id_solicitacao,
            'tipo_conta': s.tipo_conta,
            'valor_inicial': float(s.valor_inicial or 0),
            'data_solicitacao': s.data_solicitacao.isoformat(),
            'nome_cliente': s.nome_cliente
        } for s in solicitacoes]

    finally:
        db.close()

def aprovar_solicitacao(id_solicitacao, id_funcionario):
    db = SessionLocal()
    try:
        solicitacao = db.query(SolicitacaoConta).get(id_solicitacao)
        if not solicitacao:
            raise ValueError('Solicitação não encontrada')
        if solicitacao.status != 'PENDENTE':
            raise ValueError('Solicitação já foi processada')

        solicitacao.status = 'APROVADO'
        solicitacao.id_funcionario_aprovador = id_funcionario
        solicitacao.data_aprovacao = datetime.now(timezone.utc)
        db.commit()
        return {'mensagem': 'Solicitação aprovada com sucesso.'}

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def rejeitar_solicitacao(id_solicitacao, id_funcionario):
    db = SessionLocal()
    try:
        solicitacao = db.query(SolicitacaoConta).get(id_solicitacao)
        if not solicitacao:
            raise ValueError('Solicitação não encontrada')
        if solicitacao.status != 'PENDENTE':
            raise ValueError('Solicitação já foi processada')

        solicitacao.status = 'REJEITADO'
        solicitacao.id_funcionario_aprovador = id_funcionario
        solicitacao.data_aprovacao = datetime.now(timezone.utc)
        db.commit()
        return {'mensagem': 'Solicitação rejeitada com sucesso.'}

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
