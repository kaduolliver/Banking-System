from flask import session
from app.database.db import SessionLocal
from app.models.endereco import Endereco
from app.models.usuario import Usuario

def add_endereco(data):
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    # Campos obrigatórios para o endereço
    cep = data.get('cep')
    logradouro = data.get('logradouro')
    numero_casa = data.get('numero_casa')
    bairro = data.get('bairro')
    estado = data.get('estado')
    complemento = data.get('complemento')  # opcional

    # Validação básica
    if not all([cep, logradouro, numero_casa, bairro, estado]):
        return {'erro': 'Campos obrigatórios ausentes.'}, 400

    db = SessionLocal()
    try:
        # Verifica se já existe endereço para o usuário
        endereco = db.query(Endereco).filter_by(id_usuario=session['id_usuario']).first()

        if endereco:
            # Atualiza os dados
            endereco.cep = cep
            endereco.logradouro = logradouro
            endereco.numero_casa = numero_casa
            endereco.bairro = bairro
            endereco.estado = estado
            endereco.complemento = complemento
            mensagem = 'Endereço atualizado com sucesso.'
        else:
            # Insere novo endereço
            endereco = Endereco(
                id_usuario=session['id_usuario'],
                cep=cep,
                logradouro=logradouro,
                numero_casa=numero_casa,
                bairro=bairro,
                estado=estado,
                complemento=complemento
            )
            db.add(endereco)
            mensagem = 'Endereço cadastrado com sucesso.'

        db.commit()
        return {'mensagem': mensagem}, 200

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500

    finally:
        db.close()

def get_endereco():
    if 'id_usuario' not in session:
        return {'erro': 'Usuário não autenticado.'}, 401

    db = SessionLocal()
    try:
        endereco = db.query(Endereco).filter_by(id_usuario=session['id_usuario']).first()
        if endereco:
            return {
                'cep': endereco.cep,
                'logradouro': endereco.logradouro,
                'numero_casa': endereco.numero_casa,
                'bairro': endereco.bairro,
                'estado': endereco.estado,
                'complemento': endereco.complemento
            }, 200
        else:
            return {'erro': 'Endereço não encontrado.'}, 404
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()


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

