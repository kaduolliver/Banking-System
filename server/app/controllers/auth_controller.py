from flask import jsonify, session
from app.database.db import db_pool
from datetime import datetime, timedelta
import bcrypt
import random
import string
import psycopg2.errors

def gerar_otp():
    return ''.join(random.choices(string.digits, k=6))

def registrar_usuario(data):
    nome = data.get('nome')
    cpf = data.get('cpf')
    nascimento = data.get('data_nascimento')
    telefone = data.get('telefone')
    tipo = data.get('tipo_usuario')
    senha = data.get('senha')

    if tipo not in ['cliente', 'funcionario']:
        return jsonify({"erro": "Tipo de usuário inválido"}), 400

    if not all([nome, cpf, nascimento, telefone, tipo, senha]):
        return jsonify({"erro": "Preencha todos os campos obrigatórios."}), 400

    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            cur.execute("""
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_usuario
            """, (nome, cpf, nascimento, telefone, tipo, senha_hash))

            id_usuario = cur.fetchone()[0]

            if tipo == 'cliente':
                cur.execute(
                    "INSERT INTO cliente (id_usuario, score_credito) VALUES (%s, %s)",
                    (id_usuario, 0)
                )
            else:
                cur.execute("""
                    INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo)
                    VALUES (%s, %s, %s)
                """, (id_usuario, f"FUNC{id_usuario}", "Funcionário"))

            conn.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso!"})

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({"erro": "CPF já registrado."}), 400

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500

    finally:
        db_pool.putconn(conn)

def login_usuario(data):
    cpf = data.get('cpf')
    senha = data.get('senha')

    if not cpf or not senha:
        return jsonify({'erro': 'CPF e senha são obrigatórios.'}), 400

    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_usuario, senha_hash FROM usuario WHERE cpf = %s", (cpf,))
            usuario = cur.fetchone()

            if not usuario:
                return jsonify({'erro': 'CPF ou senha inválidos.'}), 401

            id_usuario, senha_hash = usuario

            if not bcrypt.checkpw(senha.encode(), senha_hash.encode()):
                return jsonify({'erro': 'CPF ou senha inválidos.'}), 401

            otp = gerar_otp()
            # print(f"OTP gerado para {cpf}: {otp}")
            expiracao = datetime.now() + timedelta(minutes=5)
            

            cur.execute("""
                UPDATE usuario
                SET otp_codigo = %s, otp_expiracao = %s, otp_ativo = TRUE
                WHERE id_usuario = %s
            """, (otp, expiracao, id_usuario))

            conn.commit()

            print(f"OTP para {cpf}: {otp}")

            return jsonify({
                'mensagem': 'OTP enviado para validação.',
                'precisa_otp': True,
                'id_usuario': id_usuario
            })

    except Exception as e:
        conn.rollback()
        return jsonify({'erro': str(e)}), 500

    finally:
        db_pool.putconn(conn)

def validar_otp(data):
    cpf = data.get('cpf')
    otp = data.get('otp')

    if not cpf or not otp:
        return jsonify({'erro': 'CPF e OTP são obrigatórios.'}), 400

    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_usuario, otp_codigo, otp_expiracao
                FROM usuario
                WHERE cpf = %s AND otp_ativo = TRUE
            """, (cpf,))
            resultado = cur.fetchone()

            if not resultado:
                return jsonify({'erro': 'OTP não encontrado ou expirado.'}), 400

            id_usuario, otp_salvo, expiracao = resultado

            if datetime.now() > expiracao:
                return jsonify({'erro': 'OTP expirado.'}), 400

            if otp != otp_salvo:
                return jsonify({'erro': 'OTP inválido.'}), 400

            cur.execute("""
                UPDATE usuario
                SET otp_ativo = FALSE, otp_codigo = NULL, otp_expiracao = NULL
                WHERE id_usuario = %s
            """, (id_usuario,))
            conn.commit()

            return jsonify({'mensagem': 'Login completo!', 'id_usuario': id_usuario})

    except Exception as e:
        conn.rollback()
        return jsonify({'erro': str(e)}), 500

    finally:
        db_pool.putconn(conn)
