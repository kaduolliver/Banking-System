from sqlalchemy.exc import DBAPIError
from psycopg2.errors import RaiseException
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.models.contaInvestimento import ContaInvestimento

def realizar_deposito(id_usuario: int, data: dict):
    
    db: Session = SessionLocal()
    try:
        
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError("Cliente não encontrado.")

        id_cliente = cliente.id_cliente

        
        id_conta     = data.get("id_conta")
        numero_conta = data.get("numero_conta")
        if not id_conta and not numero_conta:
            raise ValueError("Informe 'id_conta' ou 'numero_conta'.")

        query = db.query(Conta).filter_by(id_cliente=id_cliente)
        conta = (
            query.filter_by(id_conta=id_conta).first()
            if id_conta
            else query.filter_by(numero_conta=numero_conta).first()
        )
        if not conta:
            raise ValueError("Conta não encontrada ou não pertence ao cliente.")

        
        valor = data.get("valor")
        if valor is None:
            raise ValueError("Valor do depósito não informado.")
        valor_decimal = Decimal(str(valor))
        if valor_decimal <= 0:
            raise ValueError("Valor do depósito deve ser positivo.")

       
        if conta.tipo_conta == 'investimento':
            inv = db.query(ContaInvestimento).filter_by(id_conta=conta.id_conta).first()
            if inv and valor_decimal < inv.valor_minimo:
                raise ValueError(f"Depósito mínimo para conta investimento é {inv.valor_minimo}")

      
        nova_tx = Transacao(
            id_conta_origem = conta.id_conta,
            id_conta_destino=conta.id_conta,
            tipo_transacao='deposito',
            valor=valor_decimal,
            descricao=data.get("descricao", "Depósito via app"),
        )
        db.add(nova_tx)
        db.commit()

        return {"mensagem": f"Deposito de R$ {valor_decimal} registrado com sucesso."}

    except DBAPIError as e:
        db.rollback()
        
        if isinstance(e.orig, RaiseException) and "Limite de depósito diário" in str(e.orig):
            
            raise ValueError("Limite diário de depósito atingido para esta conta. Por favor, tente um valor menor ou outro dia.")
        else:
           
            raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def deposito_por_qr(data: dict):
    
    id_usuario = data.get("id_usuario")
    if not id_usuario:
        raise ValueError("ID do usuário não informado no token.")

    return realizar_deposito(id_usuario, data)
