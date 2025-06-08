from app.database.db import SessionLocal
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.utils.security import hash_senha, gerar_otp, verificar_senha
from app.utils.validators import validar_data, validar_campos_obrigatorios, validar_cpf
from app.utils.employee_functions import gerar_codigo_estagiario
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from flask import session

def registrar_usuario(data):
    db = SessionLocal()
    try:
        obrigatorios = ['nome', 'cpf', 'data_nascimento', 'telefone', 'tipo_usuario', 'senha']
        ok, msg = validar_campos_obrigatorios(data, obrigatorios)
        if not ok:
            return {"erro": msg}, 400

        nome = data['nome']
        cpf = data['cpf']
        tipo = data['tipo_usuario']
        senha = data['senha']

        if tipo not in ['cliente', 'funcionario']:
            return {"erro": "Tipo de usuário inválido"}, 400

        if not validar_cpf(cpf):
            return {"erro": "CPF inválido. Deve conter 11 dígitos numéricos."}, 400

        nascimento = validar_data(data['data_nascimento'])
        if not nascimento:
            return {"erro": "Data de nascimento inválida. Use o formato YYYY-MM-DD."}, 400

        senha_hash = hash_senha(senha)

        novo_usuario = Usuario(
            nome=nome,
            cpf=cpf,
            data_nascimento=nascimento,
            telefone=data['telefone'],
            tipo_usuario=tipo,
            senha_hash=senha_hash
        )

        db.add(novo_usuario)
        db.flush()

        if tipo == 'cliente':
            db.add(Cliente(id_usuario=novo_usuario.id_usuario, score_credito=0))
        else:
            codigo_gerado = gerar_codigo_estagiario(db)
            db.add(Funcionario(
                id_usuario=novo_usuario.id_usuario,
                codigo_funcionario=codigo_gerado,
                cargo="Estagiário",
                nivel_hierarquico=1,
                id_supervisor=None  
            ))


        db.commit()
        return {"mensagem": "Usuário registrado com sucesso!"}, 200

    except IntegrityError:
        db.rollback()
        return {"erro": "CPF já registrado."}, 400
    except Exception as e:
        db.rollback()
        return {"erro": str(e)}, 500
    finally:
        db.close()


def login_usuario(data):
    db = SessionLocal()
    try:
        obrigatorios = ['cpf', 'senha']
        ok, msg = validar_campos_obrigatorios(data, obrigatorios)
        if not ok:
            return {'erro': msg}, 400

        usuario = db.query(Usuario).filter_by(cpf=data['cpf']).first()
        if not usuario or not verificar_senha(data['senha'], usuario.senha_hash):
            return {'erro': 'CPF ou senha inválidos.'}, 401

        otp = gerar_otp()
        expiracao = datetime.now() + timedelta(minutes=5)

        usuario.otp_codigo = otp
        usuario.otp_expiracao = expiracao
        usuario.otp_ativo = True

        db.commit()

        print(f"OTP para {usuario.cpf}: {otp}")

        cargo = None
        if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
            cargo = usuario.funcionario.cargo

        return {
            'mensagem': 'OTP enviado para validação.',
            'precisa_otp': True,
            'id_usuario': usuario.id_usuario,
            'tipo': usuario.tipo_usuario,
            'nome': usuario.nome,
            'cpf': usuario.cpf,
            'data_nascimento': usuario.data_nascimento.isoformat(),
            'telefone': usuario.telefone,
            'cargo': cargo
        }, 200
    
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


def validar_otp(data):
    db = SessionLocal()
    try:
        ok, msg = validar_campos_obrigatorios(data, ['cpf', 'otp'])
        if not ok:
            return {'erro': msg}, 400

        usuario = db.query(Usuario).filter_by(cpf=data['cpf'], otp_ativo=True).first()
        if not usuario or usuario.otp_codigo != data['otp']:
            return {'erro': 'OTP inválido ou não encontrado.'}, 400

        if datetime.now() > usuario.otp_expiracao:
            return {'erro': 'OTP expirado.'}, 400

        usuario.otp_codigo = None
        usuario.otp_expiracao = None
        usuario.otp_ativo = False

        session['id_usuario'] = usuario.id_usuario
        session['tipo'] = usuario.tipo_usuario

        db.commit()

        cargo = None
        if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
            cargo = usuario.funcionario.cargo

        return {
            'mensagem': 'Login completo!',
            'id_usuario': usuario.id_usuario,
            'cpf': usuario.cpf,
            'telefone': usuario.telefone,
            'tipo': usuario.tipo_usuario,
            'data_nascimento': usuario.data_nascimento.isoformat(),
            'nome': usuario.nome,
            'cargo': cargo
        }, 200
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


def verificar_sessao():
    if 'id_usuario' not in session:
        return {'autenticado': False}, 401

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id_usuario=session['id_usuario']).first()
        if not usuario:
            return {'erro': 'Usuário não encontrado'}, 404

        cargo = None
        if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
            cargo = usuario.funcionario.cargo

        return {
            'autenticado': True,
            'usuario': {
                'id_usuario': usuario.id_usuario,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'telefone': usuario.telefone,
                'data_nascimento': usuario.data_nascimento.isoformat(),
                'tipo_usuario': usuario.tipo_usuario,
                'cargo': cargo
            }
        }, 200
    finally:
        db.close()
