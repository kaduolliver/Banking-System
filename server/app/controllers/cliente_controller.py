from flask import jsonify
from app.database.db import SessionLocal
from app.models.conta import Conta
from app.models.cliente import Cliente

def verificar_se_tem_conta(id_usuario):
    db = SessionLocal()
    try:
        conta = (
            db.query(Conta)
            .join(Cliente, Conta.id_cliente == Cliente.id_cliente)
            .filter(Cliente.id_usuario == id_usuario)
            .first()
        )
        return jsonify({'tem_conta': bool(conta)}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao verificar conta: {str(e)}'}), 500
    finally:
        db.close()

def solicitar_abertura_conta(id_usuario):
    db = SessionLocal()
    try:
        conta_existente = (
            db.query(Conta)
            .join(Cliente, Conta.id_cliente == Cliente.id_cliente)
            .filter(Cliente.id_usuario == id_usuario)
            .first()
        )

        if conta_existente:
            return jsonify({'erro': 'Usuário já possui uma conta ativa.'}), 400

        return jsonify({'mensagem': 'Solicitação de abertura de conta registrada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao solicitar abertura de conta: {str(e)}'}), 500
    finally:
        db.close()
