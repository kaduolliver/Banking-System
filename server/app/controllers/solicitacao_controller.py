from flask import session
from app.database.db import SessionLocal
from app.models.solicitacao import SolicitacaoConta
from app.models.cliente import Cliente
from datetime import datetime, timezone

def solicitar_abertura_conta(data):
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    tipo_conta = data.get('tipo_conta')
    tipos_validos = ['corrente', 'poupanca', 'investimento']

    if tipo_conta not in tipos_validos:
        return {'erro': 'Tipo de conta inválido.'}, 400

    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=session['id_usuario']).first()
        if not cliente:
            return {'erro': 'Cliente não encontrado.'}, 404

        cliente_id = cliente.id_cliente

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
        return {'erro': str(e)}, 500
    finally:
        db.close()



def verificar_possui_conta(_):
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    from app.models.conta import Conta
    from app.models.cliente import Cliente

    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=session['id_usuario']).first()
        if not cliente:
            return {'erro': 'Cliente não encontrado.'}, 404

        conta = db.query(Conta).filter_by(id_cliente=cliente.id_cliente).first()
        tem_conta = conta is not None
        return {'temConta': tem_conta}, 200
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()


def aprovar_solicitacao(id_solicitacao, funcionario_id):
    from app.models.conta import Conta
    from app.models.solicitacao import SolicitacaoConta

    db = SessionLocal()
    try:
        solicitacao = db.query(SolicitacaoConta).filter_by(id_solicitacao=id_solicitacao).first()

        if not solicitacao or solicitacao.status != 'PENDENTE':
            return {'erro': 'Solicitação não encontrada ou já processada.'}, 404

        # Cria a conta para o cliente
        nova_conta = Conta(
            id_cliente=solicitacao.id_cliente,
            tipo=solicitacao.tipo_conta,
            saldo=solicitacao.valor_inicial or 0.0,
            data_abertura=datetime.now(timezone.utc)
        )
        db.add(nova_conta)

        # Atualiza quem aprovou (opcional, caso deseje registrar auditoria)
        solicitacao.status = 'APROVADA'
        solicitacao.id_funcionario_aprovador = funcionario_id
        solicitacao.data_aprovacao = datetime.now(timezone.utc)

        db.commit()

        # Após criar a conta, exclui a solicitação
        db.delete(solicitacao)
        db.commit()

        return {'mensagem': 'Conta criada com sucesso. Solicitação aprovada.'}, 200

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()
