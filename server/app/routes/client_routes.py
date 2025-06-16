from flask import Blueprint, request, jsonify, session, send_file
from base64 import b64decode
import json
import time
from app.controllers.client_controllers.client import (
    cliente_solicitar_abertura_conta,
    cliente_verificar_possui_conta,
    cliente_solicitar_emprestimo,
    cliente_realizar_saque,
    cliente_realizar_saque_por_qr,
    cliente_realizar_deposito,
    cliente_realizar_deposito_por_qr,
    cliente_realizar_transferencia,
    cliente_obter_extrato,
    cliente_gerar_pdf_extrato
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
    if session['id_usuario'] != cliente_id:
        return jsonify({'erro': 'Acesso negado. Você não tem permissão para acessar esta conta.'}), 403
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
    
@client_bp.route('/api/transferencia', methods=['POST'])
def route_realizar_transferencia():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    
    data = request.get_json()
    resposta, status = cliente_realizar_transferencia(session['id_usuario'], data)
    return jsonify(resposta), status

@client_bp.route('/api/extrato/<int:cliente_id>', methods=['GET'])
def route_obter_extrato(cliente_id):
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    if session['id_usuario'] != cliente_id:
        return jsonify({'erro': 'Acesso negado. Você não tem permissão para acessar este extrato.'}), 403

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', default=10, type=int)

    resposta, status = cliente_obter_extrato(session['id_usuario'], start_date, end_date, limit)
    return jsonify(resposta), status

@client_bp.route('/api/extrato/<int:cliente_id>/pdf', methods=['GET'])
def route_gerar_pdf_extrato(cliente_id):
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    if session['id_usuario'] != cliente_id:
        return jsonify({'erro': 'Acesso negado. Você não tem permissão para gerar este PDF.'}), 403

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', default=10, type=int)

    pdf_buffer, status = cliente_gerar_pdf_extrato(session['id_usuario'], start_date, end_date, limit)

    if status != 200:
        return jsonify(pdf_buffer), status 

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'extrato_cliente_{cliente_id}.pdf'
    )
