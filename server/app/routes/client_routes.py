from flask import Blueprint, request, jsonify, session
from base64 import b64decode
import json
import time
from app.controllers.client_controllers.client import (
    cliente_solicitar_abertura_conta,
    cliente_verificar_possui_conta,
    cliente_solicitar_emprestimo,
    cliente_realizar_saque,
    cliente_realizar_saque_por_qr
)
from app.controllers.client_controllers.client import (
    cliente_realizar_deposito,
    cliente_realizar_deposito_por_qr,
)

client_bp = Blueprint('client', __name__)

@client_bp.route('/api/solicitacoes', methods=['POST'])
def route_solicitar_abertura():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    data = request.get_json()
    resposta, status = cliente_solicitar_abertura_conta(session['id_usuario'], data)
    return jsonify(resposta), status

@client_bp.route('/api/cliente/<int:cliente_id>/conta', methods=['GET'])
def route_verificar_conta(cliente_id):
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    resposta, status = cliente_verificar_possui_conta(session['id_usuario'])
    return jsonify(resposta), status

@client_bp.route('/api/emprestimos', methods=['POST'])
def route_solicitar_emprestimo():
    
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    data = request.get_json()
    
    resposta, status = cliente_solicitar_emprestimo(session['id_usuario'], data)
    return jsonify(resposta), status

@client_bp.route('/api/saque', methods=['GET', 'POST'])
def route_realizar_saque():
    
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401

    
    if request.method == 'GET':
        data = {
            "id_conta": request.args.get('id_conta', type=int),
            "numero_conta": request.args.get('numero_conta'),
            "valor": request.args.get('valor', type=float),
            "descricao": request.args.get('descricao')
        }
    else:  
        data = request.get_json(silent=True) or {}

    
    resposta, status = cliente_realizar_saque(session['id_usuario'], data)
    return jsonify(resposta), status


@client_bp.route('/api/saque_qr', methods=['GET'])
def route_realizar_saque_qr():
    token = request.args.get("token")
    if not token:
        return jsonify({"erro": "Token não fornecido."}), 400

    try:
        decoded = json.loads(b64decode(token).decode('utf-8'))

        if time.time() - decoded.get("ts", 0) > 60:
            return jsonify({"erro": "QR Code expirado."}), 400

        resposta, status = cliente_realizar_saque_por_qr(decoded)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"erro": f"Token inválido ou erro interno: {str(e)}"}), 400
    

@client_bp.route('/api/deposito', methods=['GET', 'POST'])
def route_realizar_deposito():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401

    if request.method == 'GET':
        data = {
            "id_conta":     request.args.get('id_conta', type=int),
            "numero_conta": request.args.get('numero_conta'),
            "valor":        request.args.get('valor', type=float),
            "descricao":    request.args.get('descricao'),
        }
    else:
        data = request.get_json(silent=True) or {}

    resposta, status = cliente_realizar_deposito(session['id_usuario'], data)
    return jsonify(resposta), status


@client_bp.route('/api/deposito_qr', methods=['GET'])
def route_realizar_deposito_qr():
    token = request.args.get("token")
    if not token:
        return jsonify({"erro": "Token não fornecido."}), 400

    try:
        decoded = json.loads(b64decode(token).decode('utf-8'))

        if time.time() - decoded.get("ts", 0) > 60:
            return jsonify({"erro": "QR Code expirado."}), 400

        resposta, status = cliente_realizar_deposito_por_qr(decoded)
        return jsonify(resposta), status

    except Exception as e:
        return jsonify({"erro": f"Token inválido ou erro interno: {str(e)}"}), 400