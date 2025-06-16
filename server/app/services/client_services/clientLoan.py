from sqlalchemy import text 
from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta

def solicitar_emprestimo(id_usuario: int, data: dict):
    
    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError('Cliente não encontrado.')

        id_cliente = cliente.id_cliente
        score_credito = cliente.score_credito if cliente.score_credito is not None else 50

        valor_solicitado = data.get('valor_solicitado')
        prazo_meses = data.get('prazo_meses')
        finalidade = data.get('finalidade')
        id_conta = data.get('id_conta')

        if not all([valor_solicitado, prazo_meses, finalidade, id_conta]):
            raise ValueError("Dados incompletos para a solicitação de empréstimo.")

        conta = db.query(Conta).filter_by(id_conta=id_conta, id_cliente=id_cliente).first()
        if not conta:
            raise ValueError("A conta selecionada não pertence a este cliente ou não existe.")

        db.execute(text(
            "CALL processar_emprestimo(:p_id_cliente, :p_id_conta, :p_valor, :p_prazo, :p_finalidade, :p_score_risco)"
        ), {
            "p_id_cliente": id_cliente,
            "p_id_conta": id_conta,
            "p_valor": valor_solicitado,
            "p_prazo": prazo_meses,
            "p_finalidade": finalidade,
            "p_score_risco": score_credito
        })
        db.commit()

        status_msg = "aprovado automaticamente (score ≥ 80)" if score_credito >= 80 else "aguardando análise manual"
        return {'mensagem': f'Solicitação de empréstimo registrada. Status inicial: {status_msg}.'}

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
