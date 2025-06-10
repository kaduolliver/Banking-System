from datetime import datetime, timezone
from app.database.db import SessionLocal
from app.models.solicitacao import SolicitacaoConta
from app.models.cliente import Cliente
from app.models.conta import Conta

def solicitar_abertura_conta(id_usuario, data):
    tipo_conta = data.get('tipo_conta')
    tipos_validos = ['corrente', 'poupanca', 'investimento']

    if tipo_conta not in tipos_validos:
        raise ValueError('Tipo de conta inválido.')

    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError('Cliente não encontrado.')

        cliente_id = cliente.id_cliente

        solicitacao_existente = db.query(SolicitacaoConta).filter_by(
            id_cliente=cliente_id,
            status='PENDENTE'
        ).first()

        if solicitacao_existente:
            raise ValueError('Já existe uma solicitação pendente para esse tipo de conta.')

        nova = SolicitacaoConta(
            id_cliente=cliente_id,
            tipo_conta=tipo_conta,
            status='PENDENTE',
            data_solicitacao=datetime.now(timezone.utc)
        )
        db.add(nova)
        db.commit()
        return {'mensagem': 'Solicitação enviada com sucesso.'}

    except:
        db.rollback()
        raise
    finally:
        db.close()

def verificar_possui_conta(id_usuario):
    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError('Cliente não encontrado.')

        conta = db.query(Conta).filter_by(id_cliente=cliente.id_cliente).first()
        return {'temConta': conta is not None}
    finally:
        db.close()
