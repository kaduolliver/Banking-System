from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from psycopg2.errors import RaiseException 

from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.models.contaCorrente import ContaCorrente

def realizar_transferencia(id_usuario: int, data: dict):

    db: Session = SessionLocal()
    try:
        
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError("Cliente não encontrado.")

        id_conta_origem = data.get("id_conta_origem")
        if not id_conta_origem:
            raise ValueError("ID da conta de origem não informado.")

        conta_origem = db.query(Conta).filter_by(
            id_conta=id_conta_origem,
            id_cliente=cliente.id_cliente
        ).first()

        if not conta_origem:
            raise ValueError("Conta de origem não encontrada ou não pertence ao cliente.")
        
        if conta_origem.tipo_conta != 'corrente':
            raise ValueError("Transferências são permitidas apenas a partir de contas correntes.")

        numero_conta_destino = data.get("numero_conta_destino")
        if not numero_conta_destino:
            raise ValueError("Número da conta de destino não informado.")
        
        if not numero_conta_destino.startswith('BR') or not numero_conta_destino[2:].isdigit():
            raise ValueError("Formato do número da conta destino inválido. Deve começar com 'BR' seguido apenas por números.")

        conta_destino = db.query(Conta).filter_by(numero_conta=numero_conta_destino).first()
        if not conta_destino:
            raise LookupError("Conta de destino não encontrada.")
        
        if conta_origem.id_conta == conta_destino.id_conta:
            raise ValueError("Não é possível transferir para a própria conta de origem.")

        valor = data.get("valor")
        if valor is None:
            raise ValueError("Valor da transferência não informado.")
        
        valor_decimal = Decimal(str(valor))
        if valor_decimal <= 0:
            raise ValueError("Valor da transferência deve ser positivo.")
        
        if valor_decimal < 10: 
            raise ValueError("Valor mínimo para transferência é R$ 10,00.")

        saldo_disponivel_origem = conta_origem.saldo
        if conta_origem.tipo_conta == 'corrente':
            conta_corrente_origem = db.query(ContaCorrente).filter_by(id_conta=conta_origem.id_conta).first()
            if conta_corrente_origem:
                saldo_disponivel_origem += conta_corrente_origem.limite

        if valor_decimal > saldo_disponivel_origem:
            raise ValueError("Saldo (incluindo limite) insuficiente na conta de origem.")

        nova_tx = Transacao(
            id_conta_origem=conta_origem.id_conta,
            id_conta_destino=conta_destino.id_conta,
            tipo_transacao='transferencia',
            valor=valor_decimal,
            descricao=data.get("descricao", "Transferência via app"),
            valor_taxa=Decimal('0.00')
        )
        db.add(nova_tx)
        db.commit()

        db.refresh(conta_origem)

        return {
            "mensagem": f"Transferência de R$ {valor_decimal:.2f} para conta {numero_conta_destino} realizada com sucesso.",
            "novo_saldo_origem": float(conta_origem.saldo)
        }

    except DBAPIError as e:
        db.rollback()
        if isinstance(e.orig, RaiseException):
            if "Saldo (incluindo limite) insuficiente" in str(e.orig):
                raise ValueError("Saldo insuficiente para a transferência.")
            else:
                raise ValueError(f"Erro no banco de dados: {str(e.orig).split('DETAIL: ')[-1].strip()}")
        else:
            print(f"Erro inesperado no banco de dados: {e}")
            raise ValueError("Ocorreu um erro no banco de dados ao processar a transferência.")
    except Exception as e:
        db.rollback()
        print(f"Erro inesperado ao realizar transferência: {e}")
        raise ValueError(f"Ocorreu um erro ao realizar a transferência: {str(e)}")
    finally:
        db.close()
