from app.database.db import SessionLocal
from app.models.endereco import Endereco
from app.models.agencia import Agencia

def add_endereco_agencia(data):
    id_agencia = data.get('id_agencia')

    if not id_agencia:
        return {'erro': 'ID da agência é obrigatório.'}, 400

    cep = data.get('cep')
    logradouro = data.get('logradouro')
    numero_casa = data.get('numero_casa')
    bairro = data.get('bairro')
    estado = data.get('estado')
    complemento = data.get('complemento')

    if not all([cep, logradouro, numero_casa, bairro, estado]):
        return {'erro': 'Campos obrigatórios ausentes.'}, 400

    db = SessionLocal()
    try:
        agencia = db.query(Agencia).filter_by(id_agencia=id_agencia).first()
        if not agencia:
            return {'erro': 'Agência não encontrada.'}, 404

        endereco = db.query(Endereco).filter_by(id_agencia=id_agencia).first()

        if endereco:
            endereco.cep = cep
            endereco.logradouro = logradouro
            endereco.numero_casa = numero_casa
            endereco.bairro = bairro
            endereco.estado = estado
            endereco.complemento = complemento
            mensagem = 'Endereço da agência atualizado com sucesso.'
        else:
            endereco = Endereco(
                id_agencia=id_agencia,
                cep=cep,
                logradouro=logradouro,
                numero_casa=numero_casa,
                bairro=bairro,
                estado=estado,
                complemento=complemento
            )
            db.add(endereco)
            mensagem = 'Endereço da agência cadastrado com sucesso.'

        db.commit()
        return {'mensagem': mensagem}, 200

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500

    finally:
        db.close()


def get_endereco_agencia(id_agencia):
    if not id_agencia:
        return {'erro': 'ID da agência é obrigatório.'}, 400

    db = SessionLocal()
    try:
        endereco = db.query(Endereco).filter_by(id_agencia=id_agencia).first()
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
