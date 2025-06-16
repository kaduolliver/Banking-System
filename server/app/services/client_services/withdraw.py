from decimal import Decimal
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.models.contaCorrente import ContaCorrente  
from psycopg2.errors import RaiseException
from sqlalchemy.exc import DBAPIError
import datetime
from sqlalchemy import func

def realizar_saque(id_usuario: int, data: dict):
   
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
            raise ValueError("Valor do saque não informado.")
        valor_decimal = Decimal(str(valor))
        if valor_decimal <= 0:
            raise ValueError("Valor do saque deve ser positivo.")
        
        taxa_aplicada = Decimal('0.00')
        limite_transacoes_gratuitas = 5
        valor_taxa_por_excedente = Decimal('2.50')

        primeiro_dia_mes = datetime.date.today().replace(day=1)

        saques_no_mes = db.query(func.count(Transacao.id_transacao)).filter(
        Transacao.id_conta_origem == conta.id_conta,
        Transacao.tipo_transacao == 'saque',
        Transacao.data_hora >= primeiro_dia_mes
        ).scalar()

        if saques_no_mes >= limite_transacoes_gratuitas:
            taxa_aplicada = valor_taxa_por_excedente

        valor_total_debito = valor_decimal + taxa_aplicada

        saldo_disponivel = conta.saldo
        if conta.tipo_conta == 'corrente':
            cc = db.query(ContaCorrente).filter_by(id_conta=conta.id_conta).first()
            if cc:
                saldo_disponivel += cc.limite

        if valor_total_debito > saldo_disponivel:
            raise ValueError(f"Saldo (incluindo limite) insuficiente para o saque de R$ {valor_decimal:.2f} "
                             f"com taxa de R$ {taxa_aplicada:.2f} (total: R$ {valor_total_debito:.2f}).")

        descricao_saque = data.get("descricao", "Saque via app")
        if taxa_aplicada > 0:
            descricao_saque = f"{descricao_saque} (Taxa de R$ {taxa_aplicada:.2f} aplicada)"

        nova_tx = Transacao(
            id_conta_origem=conta.id_conta,
            tipo_transacao='saque',
            valor=valor_total_debito, 
            valor_taxa=taxa_aplicada, 
            descricao=descricao_saque
        )
        db.add(nova_tx)
        db.commit()
        db.refresh(conta)

        mensagem_retorno = f"Saque de R$ {valor_decimal:.2f} registrado com sucesso."
        if taxa_aplicada > 0:
            mensagem_retorno += f" Uma taxa de R$ {taxa_aplicada:.2f} foi aplicada."

        return {
            "mensagem": mensagem_retorno,
            "novo_saldo": float(conta.saldo),
            "valor_taxa": float(taxa_aplicada)
        }

    except DBAPIError as e:
        db.rollback()
        
        if isinstance(e.orig, RaiseException) and "Limite de saque diário" in str(e.orig):
            
            raise ValueError("Limite diário de saque atingido para esta conta. Por favor, tente um valor menor ou outro dia.")
        else:
           
            raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def saque_por_qr(data: dict):
    
    db: Session = SessionLocal()
    try:
        id_usuario = data.get("id_usuario")
        if not id_usuario:
            raise ValueError("ID do usuário não informado no token.")
        
        return realizar_saque(id_usuario, data)
    except Exception as e:
        return {"erro": f"Erro ao realizar saque por QR: {str(e)}"}
    finally:
        db.close()