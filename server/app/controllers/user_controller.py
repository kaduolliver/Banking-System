from flask import session
from app.database.db import SessionLocal
from app.models.usuario import Usuario

def atualizar_usuario(data):
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    telefone = data.get('telefone')

    if not telefone:
        return {'erro': 'Telefone é obrigatório.'}, 400

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id_usuario=session['id_usuario']).first()
        if not usuario:
            return {'erro': 'Usuário não encontrado.'}, 404

        usuario.telefone = telefone
        db.commit()
        return {'mensagem': 'Telefone atualizado com sucesso.'}, 200
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()

