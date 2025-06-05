from flask import jsonify
from app.database.db import SessionLocal
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from datetime import datetime, timedelta
from flask import session
import bcrypt
import random
import string
from sqlalchemy.exc import IntegrityError

def gerar_otp():
    return ''.join(random.choices(string.digits, k=6))

def registrar_usuario(data):
    session = SessionLocal()
    try:
        nome = data.get('nome')
        cpf = data.get('cpf')
        nascimento_str = data.get('data_nascimento')
        telefone = data.get('telefone')
        tipo = data.get('tipo_usuario')
        senha = data.get('senha')

        if tipo not in ['cliente', 'funcionario']:
            return jsonify({"erro": "Tipo de usuário inválido"}), 400

        if not all([nome, cpf, nascimento_str, telefone, tipo, senha]):
            return jsonify({"erro": "Preencha todos os campos obrigatórios."}), 400
        
        try:
            nascimento = datetime.strptime(nascimento_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"erro": "Data de nascimento em formato inválido. Use YYYY-MM-DD."}), 400

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

        novo_usuario = Usuario(
            nome=nome,
            cpf=cpf,
            data_nascimento=nascimento,
            telefone=telefone,
            tipo_usuario=tipo,
            senha_hash=senha_hash
        )

        session.add(novo_usuario)
        session.flush() 

        if tipo == 'cliente':
            cliente = Cliente(id_usuario=novo_usuario.id_usuario, score_credito=0)
            session.add(cliente)
        else:
            funcionario = Funcionario(
                id_usuario=novo_usuario.id_usuario,
                codigo_funcionario=f"FUNC{novo_usuario.id_usuario}",
                cargo="Funcionário"
            )
            session.add(funcionario)

        session.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso!"})

    except IntegrityError:
        session.rollback()
        return jsonify({"erro": "CPF já registrado."}), 400

    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500

    finally:
        session.close()

def login_usuario(data):
    session = SessionLocal()
    try:
        cpf = data.get('cpf')
        senha = data.get('senha')

        if not cpf or not senha:
            return jsonify({'erro': 'CPF e senha são obrigatórios.'}), 400

        usuario = session.query(Usuario).filter_by(cpf=cpf).first()

        if not usuario or not bcrypt.checkpw(senha.encode(), usuario.senha_hash.encode()):
            return jsonify({'erro': 'CPF ou senha inválidos.'}), 401

        otp = gerar_otp()
        expiracao = datetime.now() + timedelta(minutes=5)

        usuario.otp_codigo = otp
        usuario.otp_expiracao = expiracao
        usuario.otp_ativo = True

        session.commit()

        print(f"OTP para {cpf}: {otp}")

        return jsonify({
            'mensagem': 'OTP enviado para validação.',
            'precisa_otp': True,
            'id_usuario': usuario.id_usuario,
            'tipo': usuario.tipo_usuario,
            'nome': usuario.nome,
            'cpf': usuario.cpf,
            'data_nascimento': usuario.data_nascimento.isoformat(),
            'telefone': usuario.telefone
        })

    except Exception as e:
        session.rollback()
        return jsonify({'erro': str(e)}), 500

    finally:
        session.close()

def validar_otp(data):
    session_db = SessionLocal()
    try:
        cpf = data.get('cpf')
        otp = data.get('otp')

        if not cpf or not otp:
            return jsonify({'erro': 'CPF e OTP são obrigatórios.'}), 400

        usuario = session_db.query(Usuario).filter_by(cpf=cpf, otp_ativo=True).first()

        if not usuario or usuario.otp_codigo != otp:
            return jsonify({'erro': 'OTP inválido ou não encontrado.'}), 400

        if datetime.now() > usuario.otp_expiracao:
            return jsonify({'erro': 'OTP expirado.'}), 400

        usuario.otp_codigo = None
        usuario.otp_expiracao = None
        usuario.otp_ativo = False
        session['id_usuario'] = usuario.id_usuario  
        session['tipo'] = usuario.tipo_usuario

        session_db.commit()

        return jsonify({
            'mensagem': 'Login completo!',
            'id_usuario': usuario.id_usuario,
            'cpf': usuario.cpf,
            'telefone': usuario.telefone,
            'tipo': usuario.tipo_usuario,
            'data_nascimento': usuario.data_nascimento.isoformat(),
            'nome': usuario.nome
        })

    except Exception as e:
        session_db.rollback()
        return jsonify({'erro': str(e)}), 500

    finally:
        session_db.close()