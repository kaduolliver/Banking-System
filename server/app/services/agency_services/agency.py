from app.database.db import SessionLocal
from app.models.endereco import Endereco
from app.models.agencia import Agencia
from sqlalchemy.exc import IntegrityError 

def listar_agencias():
    db = SessionLocal()
    try:
        agencias = db.query(Agencia).all()
        return [{
            'id_agencia': a.id_agencia,
            'nome': a.nome,
            'codigo_agencia': a.codigo_agencia
        } for a in agencias]
    finally:
        db.close()

def add_endereco_agencia(agencia_id, data):
    db = SessionLocal()
    try:
        
        required_fields = ['cep', 'logradouro', 'numero_casa', 'bairro', 'estado']
        if not all(field in data and data[field] for field in required_fields):
            return {'erro': 'Campos obrigatórios ausentes.'}, 400

        
        agencia = db.query(Agencia).filter_by(id_agencia=agencia_id).first()
        if not agencia:
            return {'erro': 'Agência não encontrada.'}, 404

    
        existing_endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if existing_endereco:
            
            
            return {'erro': 'Endereço já cadastrado para esta agência. Use PUT para atualizar.'}, 409 

        endereco = Endereco(
            id_agencia=agencia_id,
            cep=data.get('cep'),
            logradouro=data.get('logradouro'),
            numero_casa=data.get('numero_casa'),
            bairro=data.get('bairro'),
            estado=data.get('estado'),
            complemento=data.get('complemento')
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco) 
        return {
            'mensagem': 'Endereço da agência cadastrado com sucesso.',
            'id_endereco': endereco.id_endereco, 
            'cep': endereco.cep,
            'logradouro': endereco.logradouro,
            'numero_casa': endereco.numero_casa,
            'bairro': endereco.bairro,
            'estado': endereco.estado,
            'complemento': endereco.complemento
        }, 201 

    except IntegrityError as e:
        db.rollback()
        
        return {'erro': 'Erro de integridade ao cadastrar endereço: ' + str(e)}, 400
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()

def update_endereco_agencia(agencia_id, data):
    db = SessionLocal()
    try:
       
        if not data:
            return {'erro': 'Nenhum dado fornecido para atualização.'}, 400

        
        agencia = db.query(Agencia).filter_by(id_agencia=agencia_id).first()
        if not agencia:
            return {'erro': 'Agência não encontrada.'}, 404

        
        endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if not endereco:
            
            return {'erro': 'Endereço não encontrado para esta agência. Use POST para cadastrar.'}, 404

        
        endereco.cep = data.get('cep', endereco.cep)
        endereco.logradouro = data.get('logradouro', endereco.logradouro)
        endereco.numero_casa = data.get('numero_casa', endereco.numero_casa)
        endereco.bairro = data.get('bairro', endereco.bairro)
        endereco.estado = data.get('estado', endereco.estado)
        endereco.complemento = data.get('complemento', endereco.complemento) 

        db.commit()
        db.refresh(endereco) 

        return {
            'mensagem': 'Endereço da agência atualizado com sucesso.',
            'id_endereco': endereco.id_endereco,
            'cep': endereco.cep,
            'logradouro': endereco.logradouro,
            'numero_casa': endereco.numero_casa,
            'bairro': endereco.bairro,
            'estado': endereco.estado,
            'complemento': endereco.complemento
        }, 200 

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


def get_endereco_agencia(agencia_id):
    db = SessionLocal()
    try:
        
        endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if endereco:
            return {
                'id_endereco': endereco.id_endereco,
                'cep': endereco.cep,
                'logradouro': endereco.logradouro,
                'numero_casa': endereco.numero_casa,
                'bairro': endereco.bairro,
                'estado': endereco.estado,
                'complemento': endereco.complemento
            }, 200
        else:
            
            return {'erro': 'Endereço não encontrado para a agência.'}, 404
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()