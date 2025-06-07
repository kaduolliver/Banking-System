from flask import session
from app.database.db import SessionLocal
from app.models.solicitacao import SolicitacaoConta
from datetime import datetime, timezone

def solicitar_abertura_conta(data):
    #from flask import current_app
    #current_app.logger.info(f"Dados recebidos para solicitação: {data}")

    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    cliente_id = data.get('cliente_id')
    tipo_conta = data.get('tipo_conta')

    tipos_validos = ['corrente', 'poupanca', 'investimento']

    if not cliente_id or tipo_conta not in tipos_validos:
        #current_app.logger.error("Dados inválidos para solicitação")
        return {'erro': 'Dados inválidos para solicitação.'}, 400

    db = SessionLocal()
    try:
        solicitacao_existente = db.query(SolicitacaoConta).filter_by(
            id_cliente=cliente_id,
            status='PENDENTE'
        ).first()

        if solicitacao_existente:
            return {'erro': 'Já existe uma solicitação pendente para esse tipo de conta.'}, 400

        nova = SolicitacaoConta(
            id_cliente=cliente_id,
            tipo_conta=tipo_conta,
            status='PENDENTE',
            data_solicitacao=datetime.now(timezone.utc)
        )
        db.add(nova)
        db.commit()
        return {'mensagem': 'Solicitação enviada com sucesso.'}, 201

    except Exception as e:
        db.rollback()
        #current_app.logger.error(f"Erro ao criar solicitação: {e}")
        return {'erro': str(e)}, 500
    finally:
        db.close()



def verificar_possui_conta(cliente_id):
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    from app.models.conta import Conta 
    db = SessionLocal()
    try:
        conta = db.query(Conta).filter_by(id_cliente=cliente_id).first()
        tem_conta = conta is not None
        return {'temConta': tem_conta}, 200
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()
