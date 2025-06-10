from app.database.db import SessionLocal
from app.models.endereco import Endereco
from app.models.agencia import Agencia
from sqlalchemy.exc import IntegrityError # Importe IntegrityError para erros de unicidade

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

# Função para CADASTRAR um novo endereço (POST)
# Agora recebe agencia_id como argumento da URL
def add_endereco_agencia(agencia_id, data):
    db = SessionLocal()
    try:
        # Validação de campos obrigatórios (agora mais concisa)
        required_fields = ['cep', 'logradouro', 'numero_casa', 'bairro', 'estado']
        if not all(field in data and data[field] for field in required_fields):
            return {'erro': 'Campos obrigatórios ausentes.'}, 400

        # Verifica se a agência existe
        agencia = db.query(Agencia).filter_by(id_agencia=agencia_id).first()
        if not agencia:
            return {'erro': 'Agência não encontrada.'}, 404

        # Verifica se já existe um endereço para esta agência (evita duplicidade para POST)
        existing_endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if existing_endereco:
            # Se já existe, significa que o POST está tentando criar algo que já existe.
            # O correto seria usar PUT para atualização.
            return {'erro': 'Endereço já cadastrado para esta agência. Use PUT para atualizar.'}, 409 # 409 Conflict

        # Cria um novo endereço
        endereco = Endereco(
            id_agencia=agencia_id, # Usando o agencia_id da URL
            cep=data.get('cep'),
            logradouro=data.get('logradouro'),
            numero_casa=data.get('numero_casa'),
            bairro=data.get('bairro'),
            estado=data.get('estado'),
            complemento=data.get('complemento')
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco) # Recarrega o objeto para ter o id_endereco gerado

        return {
            'mensagem': 'Endereço da agência cadastrado com sucesso.',
            'id_endereco': endereco.id_endereco, # Retorna o ID do endereço criado
            'cep': endereco.cep,
            'logradouro': endereco.logradouro,
            'numero_casa': endereco.numero_casa,
            'bairro': endereco.bairro,
            'estado': endereco.estado,
            'complemento': endereco.complemento
        }, 201 # 201 Created

    except IntegrityError as e:
        db.rollback()
        # Captura erros de unicidade (ex: se id_agencia já tem um endereço, mas o check anterior falhou por algum motivo)
        return {'erro': 'Erro de integridade ao cadastrar endereço: ' + str(e)}, 400
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()

# Nova função para ATUALIZAR um endereço existente (PUT)
# Recebe agencia_id como argumento da URL e data com os campos a serem atualizados
def update_endereco_agencia(agencia_id, data):
    db = SessionLocal()
    try:
        # Validação de campos obrigatórios (considerando que pelo menos um pode ser atualizado)
        # Você pode ajustar essa validação para exigir todos os campos em PUT se preferir.
        if not data:
            return {'erro': 'Nenhum dado fornecido para atualização.'}, 400

        # Verifica se a agência existe (opcional, mas boa prática)
        agencia = db.query(Agencia).filter_by(id_agencia=agencia_id).first()
        if not agencia:
            return {'erro': 'Agência não encontrada.'}, 404

        # Busca o endereço existente para esta agência
        endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if not endereco:
            # Se não existe endereço, não é uma atualização (PUT), seria uma criação (POST)
            return {'erro': 'Endereço não encontrado para esta agência. Use POST para cadastrar.'}, 404

        # Atualiza os campos do endereço com os dados fornecidos
        endereco.cep = data.get('cep', endereco.cep)
        endereco.logradouro = data.get('logradouro', endereco.logradouro)
        endereco.numero_casa = data.get('numero_casa', endereco.numero_casa)
        endereco.bairro = data.get('bairro', endereco.bairro)
        endereco.estado = data.get('estado', endereco.estado)
        endereco.complemento = data.get('complemento', endereco.complemento) # Complemento pode ser nulo

        db.commit()
        db.refresh(endereco) # Recarrega o objeto após o commit

        return {
            'mensagem': 'Endereço da agência atualizado com sucesso.',
            'id_endereco': endereco.id_endereco,
            'cep': endereco.cep,
            'logradouro': endereco.logradouro,
            'numero_casa': endereco.numero_casa,
            'bairro': endereco.bairro,
            'estado': endereco.estado,
            'complemento': endereco.complemento
        }, 200 # 200 OK

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


# Função para BUSCAR o endereço (GET)
# Agora recebe id_agencia diretamente como int (já que Flask garante que é int)
def get_endereco_agencia(agencia_id):
    db = SessionLocal()
    try:
        # Não é mais necessário int(id_agencia) se a rota Flask já garante que é int
        endereco = db.query(Endereco).filter_by(id_agencia=agencia_id).first()
        if endereco:
            return {
                'id_endereco': endereco.id_endereco, # Incluindo o ID do endereço
                'cep': endereco.cep,
                'logradouro': endereco.logradouro,
                'numero_casa': endereco.numero_casa,
                'bairro': endereco.bairro,
                'estado': endereco.estado,
                'complemento': endereco.complemento
            }, 200
        else:
            # Retorna 404 se não encontrar, o que é o comportamento esperado para "não encontrado"
            return {'erro': 'Endereço não encontrado para a agência.'}, 404
    except Exception as e:
        return {'erro': str(e)}, 500
    finally:
        db.close()