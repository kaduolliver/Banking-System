# app/services/client_services/saque.py
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.models.contaCorrente import ContaCorrente  # ajuste: nome do model = conta_corrente.py

def realizar_saque(id_usuario: int, data: dict):
    """
    Realiza um saque (com uso de limite se for conta corrente).
    Espera no JSON:
      - id_conta ou numero_conta
      - valor
      - descricao (opcional)
    """
    db: Session = SessionLocal()
    try:
        # 1) Valida cliente
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError("Cliente não encontrado.")

        id_cliente = cliente.id_cliente

        # 2) Encontra conta
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

        # 3) Valida valor e saldo + limite
        valor = data.get("valor")
        if valor is None:
            raise ValueError("Valor do saque não informado.")
        valor_decimal = Decimal(str(valor))
        if valor_decimal <= 0:
            raise ValueError("Valor do saque deve ser positivo.")

        saldo_disponivel = conta.saldo
        if conta.tipo_conta == 'corrente':
            cc = db.query(ContaCorrente).filter_by(id_conta=conta.id_conta).first()
            if cc:
                saldo_disponivel += cc.limite

        if valor_decimal > saldo_disponivel:
            raise ValueError("Saldo (incluindo limite) insuficiente.")

        # 4) Insere transação; trigger fará o débito no banco
        nova_tx = Transacao(
            id_conta_origem=conta.id_conta,
            tipo_transacao='saque',
            valor=valor_decimal,
            descricao=data.get("descricao", "Saque via app")
        )
        db.add(nova_tx)
        db.commit()

        return {"mensagem": f"Saque de R$ {valor_decimal} registrado com sucesso."}

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def saque_por_qr(data: dict):
    """
    Realiza saque pelo token QR code decodificado.
    Espera um dict com:
      - id_usuario
      - id_conta ou numero_conta
      - valor
      - descricao (opcional)
      - ts (timestamp)
    """
    db: Session = SessionLocal()
    try:
        # Valida dados mínimos
        id_usuario = data.get("id_usuario")
        if not id_usuario:
            raise ValueError("ID do usuário não informado no token.")
        
        # Você pode usar a função realizar_saque para reaproveitar lógica,
        # mas precisa garantir que o usuário existe e que os dados estão corretos
        return realizar_saque(id_usuario, data)
    except Exception as e:
        raise
    finally:
        db.close()