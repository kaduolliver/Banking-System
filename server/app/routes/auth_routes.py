from flask import Blueprint, request, jsonify
from app.database.db import db_pool
import bcrypt
import psycopg2.errors

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
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
                cur.execute("INSERT INTO cliente (id_usuario, score_credito) VALUES (%s, %s)", (id_usuario, 0))
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
