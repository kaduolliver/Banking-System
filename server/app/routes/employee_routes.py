from flask import Blueprint, jsonify, session, send_file, request
from datetime import datetime
from app.controllers.employee_controllers.employee import (
    employee_listar_solicitacoes_pendentes,
    employee_aprovar_solicitacao,
    employee_rejeitar_solicitacao,
    employee_listar_funcionarios,
    employee_atualizar_status,
    employee_listar_emprestimos_pendentes,
    employee_decidir_emprestimo,
    employee_listar_tipos_relatorio,
    employee_gerar_relatorio,
    employee_gerar_pdf_relatorio
)

employee_bp = Blueprint('funcionario', __name__)

# Checagem funcionario autenticado
@employee_bp.before_request
def check_funcionario_auth():
    if request.method == 'OPTIONS':
        return None 
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Usuário não autenticado.'}), 401
    
#----------------------------------------------------------------------------------------

# Rotas Solicitações de Contas
@employee_bp.route('/api/solicitacoes/pendentes', methods=['GET'])
def route_listar_solicitacoes_pendentes():
    resposta, status = employee_listar_solicitacoes_pendentes()
    return jsonify(resposta), status

@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/aprovar', methods=['POST'])
def route_aprovar_solicitacao(id_solicitacao):
    funcionario_id = session.get('id_funcionario')
    if not funcionario_id: 
        return jsonify({'erro': 'ID do funcionário não disponível na sessão.'}), 400

    resposta, status = employee_aprovar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status

@employee_bp.route('/api/solicitacoes/<int:id_solicitacao>/rejeitar', methods=['POST'])
def route_rejeitar_solicitacao(id_solicitacao):
    funcionario_id = session.get('id_funcionario')
    if not funcionario_id:
        return jsonify({'erro': 'ID do funcionário não disponível na sessão.'}), 400

    resposta, status = employee_rejeitar_solicitacao(id_solicitacao, funcionario_id)
    return jsonify(resposta), status

#----------------------------------------------------------------------------------------

# Rotas do Painel de controle de funcionários (ADM)
@employee_bp.route('/api/employees', methods=['GET'])
def route_listar_funcionarios():
    cargo = session.get('cargo')
    if not cargo or cargo not in ['Admin']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores podem listar funcionários.'}), 403

    resposta, status = employee_listar_funcionarios()
    return jsonify(resposta), status

@employee_bp.route('/api/employees/<int:id_funcionario>/status', methods=['PUT']) 
def route_atualizar_status(id_funcionario):
    cargo = session.get('cargo')
    if not cargo or cargo not in ['Admin']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores podem atualizar status.'}), 403

    resposta, status = employee_atualizar_status(id_funcionario)
    return jsonify(resposta), status
#----------------------------------------------------------------------------------------


# Rotas de Solicitações de empréstimos manuais
@employee_bp.route('/api/emprestimos/pendentes', methods=['GET'])
def route_listar_emprestimos_pendentes():
    resposta, status = employee_listar_emprestimos_pendentes()
    return jsonify(resposta), status

@employee_bp.route('/api/emprestimos/<int:id_emprestimo>/decidir', methods=['PUT'])
def route_decidir_emprestimo(id_emprestimo):
    funcionario_id = session.get('id_funcionario')
    if not funcionario_id:
        return jsonify({'erro': 'ID do funcionário não disponível na sessão.'}), 400

    resposta, status = employee_decidir_emprestimo(id_emprestimo, funcionario_id)
    return jsonify(resposta), status

#----------------------------------------------------------------------------------------

# Rotas de Relatório
@employee_bp.route('/api/funcionario/relatorios/tipos', methods=['GET'])
def route_listar_tipos_relatorio():
    id_usuario = session.get('id_usuario') 
    if not id_usuario:
        return jsonify({'erro': 'ID do usuário não disponível na sessão.'}), 400

    resposta, status = employee_listar_tipos_relatorio(id_usuario) 
    return jsonify(resposta), status

@employee_bp.route('/api/funcionario/relatorios/gerar', methods=['POST'])
def route_gerar_relatorio():
    data = request.get_json()
    resposta, status = employee_gerar_relatorio(session['id_usuario'], data)
    return jsonify(resposta), status

@employee_bp.route('/api/funcionario/relatorios/pdf', methods=['POST'])
def route_gerar_pdf_relatorio():
    data = request.get_json()
    pdf_buffer, status = employee_gerar_pdf_relatorio(session['id_usuario'], data)

    if status != 200:
        return jsonify(pdf_buffer), status 

    report_type_name = data.get('tipo_relatorio', 'relatorio_generico')
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'relatorio_{report_type_name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    )

#----------------------------------------------------------------------------------------