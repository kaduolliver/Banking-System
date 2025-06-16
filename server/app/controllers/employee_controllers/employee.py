from flask import session, request
from app.database.db import SessionLocal
from app.models.funcionario import Funcionario
from app.models.usuario import Usuario
from app.services.employee_services.adm_config import listar_funcionarios, atualizar_status_funcionario
from app.services.employee_services.empRequest import (
    listar_solicitacoes_pendentes,
    aprovar_solicitacao,
    rejeitar_solicitacao
)
from app.services.employee_services.empLoan import (
    listar_emprestimos_pendentes,
    decidir_emprestimo
)
from app.services.employee_services.report import (
    obter_lista_tipos_relatorio,
    gerar_relatorio,
    gerar_pdf_relatorio
)

def _verificar_permissao(cargos_permitidos):
    if not session.get('id_funcionario') or session.get('cargo') not in cargos_permitidos:
        return False
    return True

def employee_listar_solicitacoes_pendentes():
    try:
        resultado = listar_solicitacoes_pendentes()
        return resultado, 200
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_aprovar_solicitacao(id_solicitacao, id_funcionario):
    if not _verificar_permissao(['Admin', 'Gerente']):
        return {'erro': 'Acesso negado.'}, 403

    try:
        resultado = aprovar_solicitacao(id_solicitacao, id_funcionario)
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 400
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_rejeitar_solicitacao(id_solicitacao, id_funcionario):
    if not _verificar_permissao(['Admin', 'Gerente']):
        return {'erro': 'Acesso negado.'}, 403

    try:
        resultado = rejeitar_solicitacao(id_solicitacao, id_funcionario)
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 400
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_listar_funcionarios():
    if not _verificar_permissao(['Admin']):
        return {'erro': 'Acesso negado.'}, 403

    try:
        funcionarios = listar_funcionarios()
        return funcionarios, 200
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_atualizar_status(id_funcionario):
    if not _verificar_permissao(['Admin']):
        return {'erro': 'Acesso negado.'}, 403

    dados = request.get_json()
    if dados is None or 'inativo' not in dados:
        return {'erro': 'Campo "inativo" é obrigatório.'}, 400

    try:
        resultado = atualizar_status_funcionario(id_funcionario, dados['inativo'])
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 404
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_listar_emprestimos_pendentes():
    if not _verificar_permissao(['Admin', 'Gerente']):
        return {'erro': 'Acesso negado.'}, 403

    try:
        dados = listar_emprestimos_pendentes()
        return dados, 200
    except Exception as e:
        return {'erro': str(e)}, 500

def employee_decidir_emprestimo(id_emprestimo, id_funcionario):
    if not _verificar_permissao(['Admin', 'Gerente']):
        return {'erro': 'Acesso negado.'}, 403

    dados = request.get_json() or {}
    if 'aprovado' not in dados:
        return {'erro': 'Campo "aprovado" é obrigatório.'}, 400

    try:
        resultado = decidir_emprestimo(id_emprestimo, bool(dados['aprovado']), id_funcionario)
        return resultado, 200
    except ValueError as e:
        return {'erro': str(e)}, 400
    except Exception as e:
        return {'erro': str(e)}, 500

PERMISSOES_RELATORIOS = {
    "movimentacoes_financeiras": ['Admin', 'Gerente', 'Estagiário'], 
    "solicitacoes_abertura_conta": ['Admin', 'Gerente'],
    "solicitacoes_emprestimo": ['Admin', 'Gerente'],
    "status_funcionarios": ['Admin'],
    "auditoria_geral": ['Admin'],
}

def employee_listar_tipos_relatorio(id_usuario: int):

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if not usuario or usuario.tipo_usuario != 'funcionario':
            return {"erro": "Acesso negado. Usuário não é um funcionário."}, 403
        
        funcionario = db.query(Funcionario).filter_by(id_usuario=id_usuario).first()
        if not funcionario:
            return {"erro": "Funcionário não encontrado."}, 404

        cargo_funcionario = funcionario.cargo

        tipos_disponiveis = []
        todos_tipos = obter_lista_tipos_relatorio()

        for tipo_relatorio in todos_tipos:
            relatorio_id = tipo_relatorio['id']
    
            if cargo_funcionario in PERMISSOES_RELATORIOS.get(relatorio_id, []):
                tipos_disponiveis.append(tipo_relatorio)
        
        return tipos_disponiveis, 200
    except Exception as e:
        return {"erro": str(e)}, 500
    finally:
        db.close()


def employee_gerar_relatorio(id_usuario: int, data: dict):

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if not usuario or usuario.tipo_usuario != 'funcionario':
            raise ValueError("Apenas funcionários podem gerar relatórios.")
        
        funcionario = db.query(Funcionario).filter_by(id_usuario=id_usuario).first()
        if not funcionario:
            raise LookupError("Funcionário não encontrado para o ID de usuário fornecido.")

        tipo_relatorio = data.get('tipo_relatorio')
        
        
        cargo_funcionario = funcionario.cargo
        if not tipo_relatorio or cargo_funcionario not in PERMISSOES_RELATORIOS.get(tipo_relatorio, []):
            raise ValueError(f"Acesso negado. Seu cargo ({cargo_funcionario}) não tem permissão para gerar este relatório.")
       

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        limit = data.get('limit', 10)

        filtros_especificos = {k: v for k, v in data.items() if k not in ['tipo_relatorio', 'start_date', 'end_date', 'limit']}

        report_data_json = gerar_relatorio(
            funcionario.id_funcionario,
            tipo_relatorio,
            start_date,
            end_date,
            limit,
            **filtros_especificos
        )
        return report_data_json, 200
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
    finally:
        db.close()


def employee_gerar_pdf_relatorio(id_usuario: int, data: dict):

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if not usuario or usuario.tipo_usuario != 'funcionario':
            raise ValueError("Apenas funcionários podem gerar relatórios em PDF.")
        
        funcionario = db.query(Funcionario).filter_by(id_usuario=id_usuario).first()
        if not funcionario:
            raise LookupError("Funcionário não encontrado para o ID de usuário fornecido.")
        
        tipo_relatorio = data.get('tipo_relatorio')

        
        cargo_funcionario = funcionario.cargo
        if not tipo_relatorio or cargo_funcionario not in PERMISSOES_RELATORIOS.get(tipo_relatorio, []):
            raise ValueError(f"Acesso negado. Seu cargo ({cargo_funcionario}) não tem permissão para gerar este PDF de relatório.")

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        limit = data.get('limit', 10)
        filtros_especificos = {k: v for k, v in data.items() if k not in ['tipo_relatorio', 'start_date', 'end_date', 'limit']}

        report_data_json = gerar_relatorio(
            funcionario.id_funcionario,
            tipo_relatorio,
            data.get('start_date'),
            data.get('end_date'),
            data.get('limit', 10),
            **{k: v for k, v in data.items() if k not in ['tipo_relatorio', 'start_date', 'end_date', 'limit']}
        )

        funcionario_nome = usuario.nome
        
        pdf_buffer = gerar_pdf_relatorio(report_data_json, funcionario_nome)
        return pdf_buffer, 200
    except ValueError as e:
        return {"erro": str(e)}, 400
    except LookupError as e:
        return {"erro": str(e)}, 404
    except Exception as e:
        return {"erro": str(e)}, 500
    finally:
        db.close()