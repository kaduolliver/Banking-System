import io
from datetime import datetime, timezone
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, desc, func
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import black, HexColor
from app.database.db import SessionLocal
from app.models.agencia import Agencia
from app.models.auditoria import Auditoria
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.emprestimo import Emprestimo
from app.models.funcionario import Funcionario
from app.models.relatorio import Relatorio
from app.models.solicitacao import SolicitacaoConta
from app.models.transacao import Transacao
from app.models.usuario import Usuario

def _registrar_auditoria(db: Session, id_usuario: int, acao: str, detalhes: str):
    auditoria_entry = Auditoria(
        id_usuario=id_usuario,
        acao=acao,
        detalhes=detalhes,
        data_hora=datetime.now(timezone.utc)
    )
    db.add(auditoria_entry)
    db.commit()


def obter_lista_tipos_relatorio() -> list[dict]:
    return [
        {"id": "movimentacoes_financeiras", "nome": "Movimentações Financeiras de Clientes"},
        {"id": "solicitacoes_abertura_conta", "nome": "Solicitações de Abertura de Conta"},
        {"id": "solicitacoes_emprestimo", "nome": "Solicitações de Empréstimo"},
        {"id": "status_funcionarios", "nome": "Status e Ativação/Desativação de Funcionários"},
        {"id": "auditoria_geral", "nome": "Auditoria Geral do Sistema"},
    ]


def _formatar_data_hora(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else "N/A"

def _formatar_valor(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _obter_movimentacoes_financeiras(db: Session, start_date: datetime, end_date: datetime, id_agencia: int = None, id_cliente: int = None, limit: int = None):
    
    ContaOrigem = aliased(Conta)
    ContaDestino = aliased(Conta)

    query = db.query(
        Transacao.tipo_transacao,
        Transacao.valor,
        Transacao.data_hora,
        Transacao.descricao,
        ContaOrigem.numero_conta.label('conta_origem_numero'),
        ContaDestino.numero_conta.label('conta_destino_numero'),
        Usuario.nome.label('nome_cliente_origem'),
        Usuario.cpf.label('cpf_cliente_origem')
    ).join(
        ContaOrigem, Transacao.id_conta_origem == ContaOrigem.id_conta
    ).join(
        Cliente, ContaOrigem.id_cliente == Cliente.id_cliente
    ).join(
        Usuario, Cliente.id_usuario == Usuario.id_usuario
    ).outerjoin(
        ContaDestino, Transacao.id_conta_destino == ContaDestino.id_conta
    )

    if start_date:
        query = query.filter(Transacao.data_hora >= start_date)
    if end_date:
        query = query.filter(Transacao.data_hora <= end_date)
    if id_agencia:
        query = query.filter(or_(ContaOrigem.id_agencia == id_agencia, ContaDestino.id_agencia == id_agencia))
    if id_cliente:
        query = query.filter(or_(ContaOrigem.id_cliente == id_cliente, ContaDestino.id_cliente == id_cliente))

    query = query.order_by(desc(Transacao.data_hora))
    if limit:
        query = query.limit(limit)

    results = []
    for t in query.all():
        results.append({
            "tipo": t.tipo_transacao,
            "valor": _formatar_valor(t.valor),
            "data_hora": _formatar_data_hora(t.data_hora),
            "descricao": t.descricao or "N/A",
            "conta_origem": t.conta_origem_numero,
            "conta_destino": t.conta_destino_numero or "N/A",
            "cliente_origem": t.nome_cliente_origem,
            "cpf_cliente_origem": t.cpf_cliente_origem
        })
    return results


def _obter_solicitacoes_abertura_conta(db: Session, start_date: datetime, end_date: datetime, status: str = None, id_funcionario_aprovador: int = None, limit: int = None):
    
    UsuarioFunc = aliased(Usuario)

    query = db.query(
        SolicitacaoConta.id_solicitacao,
        SolicitacaoConta.tipo_conta,
        SolicitacaoConta.data_solicitacao,
        SolicitacaoConta.status,
        SolicitacaoConta.data_aprovacao,
        SolicitacaoConta.observacoes,
        SolicitacaoConta.valor_inicial,
        Usuario.nome.label('nome_cliente'),
        Usuario.cpf.label('cpf_cliente'),
        Funcionario.codigo_funcionario.label('aprovador_codigo'),
        UsuarioFunc.nome.label('aprovador_nome')
    ).join(
        Cliente, SolicitacaoConta.id_cliente == Cliente.id_cliente
    ).join(
        Usuario, Cliente.id_usuario == Usuario.id_usuario
    ).outerjoin(
        Funcionario, SolicitacaoConta.id_funcionario_aprovador == Funcionario.id_funcionario
    ).outerjoin(
        UsuarioFunc, Funcionario.id_usuario == UsuarioFunc.id_usuario
    )

    if start_date:
        query = query.filter(SolicitacaoConta.data_solicitacao >= start_date)
    if end_date:
        query = query.filter(SolicitacaoConta.data_solicitacao <= end_date)
    if status:
        query = query.filter(SolicitacaoConta.status == status.upper())
    if id_funcionario_aprovador:
        query = query.filter(SolicitacaoConta.id_funcionario_aprovador == id_funcionario_aprovador)

    query = query.order_by(desc(SolicitacaoConta.data_solicitacao))
    if limit:
        query = query.limit(limit)

    results = []
    for s in query.all():
        results.append({
            "id_solicitacao": s.id_solicitacao,
            "cliente": f"{s.nome_cliente} ({s.cpf_cliente})",
            "tipo_conta": s.tipo_conta.capitalize(),
            "data_solicitacao": _formatar_data_hora(s.data_solicitacao),
            "status": s.status,
            "valor_inicial": _formatar_valor(s.valor_inicial),
            "funcionario_aprovador": f"{s.aprovador_nome} ({s.aprovador_codigo})" if s.aprovador_nome else "N/A",
            "data_aprovacao": _formatar_data_hora(s.data_aprovacao),
            "observacoes": s.observacoes or "N/A"
        })
    return results


def _obter_solicitacoes_emprestimo(db: Session, start_date: datetime, end_date: datetime, status: str = None, id_funcionario_aprovador: int = None, limit: int = None):

    UsuarioFunc = aliased(Usuario)

    query = db.query(
        Emprestimo.id_emprestimo,
        Emprestimo.valor_solicitado,
        Emprestimo.taxa_juros_mensal,
        Emprestimo.prazo_meses,
        Emprestimo.valor_total,
        Emprestimo.data_solicitacao,
        Emprestimo.data_aprovacao,
        Emprestimo.status,
        Emprestimo.score_risco,
        Emprestimo.finalidade,
        Usuario.nome.label('nome_cliente'),
        Usuario.cpf.label('cpf_cliente'),
        Conta.numero_conta.label('numero_conta_cliente'),
        Funcionario.codigo_funcionario.label('aprovador_codigo'),
        UsuarioFunc.nome.label('aprovador_nome')
    ).join(
        Cliente, Emprestimo.id_cliente == Cliente.id_cliente
    ).join(
        Usuario, Cliente.id_usuario == Usuario.id_usuario
    ).join(
        Conta, Emprestimo.id_conta == Conta.id_conta
    ).outerjoin(
        Funcionario, Emprestimo.id_funcionario_aprovador == Funcionario.id_funcionario
    ).outerjoin(
        UsuarioFunc, Funcionario.id_usuario == UsuarioFunc.id_usuario
    )

    if start_date:
        query = query.filter(Emprestimo.data_solicitacao >= start_date)
    if end_date:
        query = query.filter(Emprestimo.data_solicitacao <= end_date)
    if status:
        query = query.filter(Emprestimo.status == status.upper())
    if id_funcionario_aprovador:
        query = query.filter(Emprestimo.id_funcionario_aprovador == id_funcionario_aprovador)

    query = query.order_by(desc(Emprestimo.data_solicitacao))
    if limit:
        query = query.limit(limit)

    results = []
    for e in query.all():
        results.append({
            "id_emprestimo": e.id_emprestimo,
            "cliente": f"{e.nome_cliente} ({e.cpf_cliente})",
            "conta_cliente": e.numero_conta_cliente,
            "valor_solicitado": _formatar_valor(e.valor_solicitado),
            "valor_total": _formatar_valor(e.valor_total),
            "taxa_juros": f"{e.taxa_juros_mensal:.2f}%",
            "prazo_meses": e.prazo_meses,
            "finalidade": e.finalidade,
            "data_solicitacao": _formatar_data_hora(e.data_solicitacao),
            "status": e.status,
            "score_risco": f"{e.score_risco:.2f}",
            "funcionario_aprovador": f"{e.aprovador_nome} ({e.aprovador_codigo})" if e.aprovador_nome else "N/A",
            "data_aprovacao": _formatar_data_hora(e.data_aprovacao)
        })
    return results


def _obter_status_funcionarios(db: Session, id_agencia: int = None, cargo: str = None, inativo: bool = None, limit: int = None):

    query = db.query(
        Funcionario.id_funcionario,
        Funcionario.codigo_funcionario,
        Funcionario.cargo,
        Funcionario.nivel_hierarquico,
        Funcionario.inativo,
        Usuario.nome.label('nome_funcionario'),
        Usuario.cpf.label('cpf_funcionario'),
        Agencia.nome.label('nome_agencia'),
        Agencia.codigo_agencia.label('codigo_agencia')
    ).join(
        Usuario, Funcionario.id_usuario == Usuario.id_usuario
    ).join(
        Agencia, Funcionario.id_agencia == Agencia.id_agencia
    )

    if id_agencia:
        query = query.filter(Funcionario.id_agencia == id_agencia)
    if cargo:
        query = query.filter(Funcionario.cargo.ilike(f"%{cargo}%"))
    if inativo is not None:
        query = query.filter(Funcionario.inativo == inativo)

    query = query.order_by(Funcionario.inativo, Funcionario.cargo, Usuario.nome)
    if limit:
        query = query.limit(limit)

    results = []
    for f in query.all():
        results.append({
            "id_funcionario": f.id_funcionario,
            "nome": f"{f.nome_funcionario} ({f.cpf_funcionario})",
            "codigo_funcionario": f.codigo_funcionario,
            "cargo": f.cargo,
            "nivel_hierarquico": f.nivel_hierarquico,
            "status": "Inativo" if f.inativo else "Ativo",
            "agencia": f"{f.nome_agencia} ({f.codigo_agencia})"
        })
    return results


def _obter_auditoria_geral(db: Session, start_date: datetime, end_date: datetime, acao: str = None, id_usuario: int = None, limit: int = None):

    query = db.query(
        Auditoria.id_auditoria,
        Auditoria.acao,
        Auditoria.data_hora,
        Auditoria.detalhes,
        Usuario.nome.label('nome_usuario_auditoria'),
        Usuario.tipo_usuario.label('tipo_usuario_auditoria')
    ).outerjoin(
        Usuario, Auditoria.id_usuario == Usuario.id_usuario
    )

    if start_date:
        query = query.filter(Auditoria.data_hora >= start_date)
    if end_date:
        query = query.filter(Auditoria.data_hora <= end_date)
    if acao:
        query = query.filter(Auditoria.acao.ilike(f"%{acao}%"))
    if id_usuario:
        query = query.filter(Auditoria.id_usuario == id_usuario)

    query = query.order_by(desc(Auditoria.data_hora))
    if limit:
        query = query.limit(limit)

    results = []
    for a in query.all():
        results.append({
            "id_auditoria": a.id_auditoria,
            "acao": a.acao,
            "data_hora": _formatar_data_hora(a.data_hora),
            "detalhes": a.detalhes or "N/A",
            "usuario": f"{a.nome_usuario_auditoria} ({a.tipo_usuario_auditoria})" if a.nome_usuario_auditoria else "N/A"
        })
    return results


def gerar_relatorio(id_funcionario_solicitante: int, tipo_relatorio: str, start_date: str = None, end_date: str = None, limit: int = 10, **kwargs):

    db: Session = SessionLocal()
    try:
        
        funcionario = db.query(Funcionario).filter_by(id_funcionario=id_funcionario_solicitante).first()
        if not funcionario:
            raise LookupError("Funcionário solicitante não encontrado.")
        
       
        data_inicio_dt = None
        data_fim_dt = None
        if start_date:
            try:
                data_inicio_dt = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Formato de data de início inválido. Use AAAA-MM-DD.")
        if end_date:
            try:
                data_fim_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            except ValueError:
                raise ValueError("Formato de data de fim inválido. Use AAAA-MM-DD.")

        report_data = []
        report_title = ""
        report_description = ""

        if tipo_relatorio == "movimentacoes_financeiras":
            report_title = "Relatório de Movimentações Financeiras de Clientes"
            report_description = "Detalhes de depósitos, saques e transferências."
            report_data = _obter_movimentacoes_financeiras(
                db, data_inicio_dt, data_fim_dt,
                id_agencia=kwargs.get('id_agencia'),
                id_cliente=kwargs.get('id_cliente'),
                limit=limit
            )
        elif tipo_relatorio == "solicitacoes_abertura_conta":
            report_title = "Relatório de Solicitações de Abertura de Conta"
            report_description = "Status e detalhes das solicitações de novas contas."
            report_data = _obter_solicitacoes_abertura_conta(
                db, data_inicio_dt, data_fim_dt,
                status=kwargs.get('status'),
                id_funcionario_aprovador=kwargs.get('id_funcionario_aprovador'),
                limit=limit
            )
        elif tipo_relatorio == "solicitacoes_emprestimo":
            report_title = "Relatório de Solicitações de Empréstimo"
            report_description = "Visão geral das solicitações de empréstimo e seus status."
            report_data = _obter_solicitacoes_emprestimo(
                db, data_inicio_dt, data_fim_dt,
                status=kwargs.get('status'),
                id_funcionario_aprovador=kwargs.get('id_funcionario_aprovador'),
                limit=limit
            )
        elif tipo_relatorio == "status_funcionarios":
            report_title = "Relatório de Status e Ativação/Desativação de Funcionários"
            report_description = "Situação atual e detalhes dos funcionários."
            report_data = _obter_status_funcionarios(
                db,
                id_agencia=kwargs.get('id_agencia'),
                cargo=kwargs.get('cargo'),
                inativo=kwargs.get('inativo'),
                limit=limit
            )
        elif tipo_relatorio == "auditoria_geral":
            report_title = "Relatório de Auditoria Geral do Sistema"
            report_description = "Registros de todas as ações auditadas no sistema."
            report_data = _obter_auditoria_geral(
                db, data_inicio_dt, data_fim_dt,
                acao=kwargs.get('acao'),
                id_usuario=kwargs.get('id_usuario'),
                limit=limit
            )
        else:
            raise ValueError("Tipo de relatório inválido.")

       
        relatorio_db = Relatorio(
            id_funcionario=id_funcionario_solicitante,
            tipo_relatorio=tipo_relatorio,
            data_geracao=datetime.now(timezone.utc),
            conteudo=f"Título: {report_title}\nDescrição: {report_description}\nDados: {report_data}"
        )
        db.add(relatorio_db)
        db.commit()

        _registrar_auditoria(
            db,
            funcionario.id_usuario,
            'GERACAO_RELATORIO',
            f"Funcionário {funcionario.codigo_funcionario} ({funcionario.cargo}) gerou o relatório: {report_title}"
        )

        return {
            "title": report_title,
            "description": report_description,
            "data": report_data,
            "filters": {
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
                **kwargs
            }
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def gerar_pdf_relatorio(report_data: dict, funcionario_nome: str):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='TitleStyle',
                             fontSize=20, leading=24, alignment=TA_CENTER,
                             spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SubtitleStyle',
                             fontSize=14, leading=16, alignment=TA_CENTER,
                             spaceAfter=10, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='NormalStyle',
                             fontSize=10, leading=12, alignment=TA_LEFT,
                             spaceAfter=5, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='HeaderStyle',
                             fontSize=10, leading=12, alignment=TA_CENTER,
                             fontName='Helvetica-Bold', textColor=black))
    styles.add(ParagraphStyle(name='DataStyle',
                             fontSize=10, leading=12, alignment=TA_LEFT,
                             fontName='Helvetica'))
    styles.add(ParagraphStyle(name='ValueStyle',
                             fontSize=10, leading=12, alignment=TA_RIGHT,
                             fontName='Helvetica'))
    styles.add(ParagraphStyle(name='FilterStyle',
                             fontSize=10, leading=12, alignment=TA_LEFT,
                             spaceAfter=5, fontName='Helvetica-Oblique', textColor=HexColor('#555555')))

    story = []

    story.append(Paragraph(report_data.get('title', 'Relatório Gerado'), styles['TitleStyle']))
    story.append(Paragraph(f"Gerado por: {funcionario_nome} em {_formatar_data_hora(datetime.now())}", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(report_data.get('description', 'N/A'), styles['NormalStyle']))
    story.append(Spacer(1, 0.1 * inch))

    filters = report_data.get('filters', {})
    if filters:
        filter_text = "Filtros: "
        filter_parts = []
        for key, value in filters.items():
            if value is not None and value != '':
                if key == 'start_date':
                    filter_parts.append(f"Data Início: {value}")
                elif key == 'end_date':
                    filter_parts.append(f"Data Fim: {value}")
                elif key == 'limit':
                    filter_parts.append(f"Limite de Registros: {value}")
                elif key == 'id_agencia':
                    filter_parts.append(f"ID Agência: {value}")
                elif key == 'id_cliente':
                    filter_parts.append(f"ID Cliente: {value}")
                elif key == 'status':
                    filter_parts.append(f"Status: {value.upper()}")
                elif key == 'id_funcionario_aprovador':
                    filter_parts.append(f"ID Func. Aprovador: {value}")
                elif key == 'cargo':
                    filter_parts.append(f"Cargo: {value}")
                elif key == 'inativo':
                    filter_parts.append(f"Status Inativo: {'Sim' if value else 'Não'}")
                elif key == 'acao':
                    filter_parts.append(f"Ação: {value}")
                elif key == 'id_usuario':
                    filter_parts.append(f"ID Usuário: {value}")
                else:
                    filter_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        if filter_parts:
            story.append(Paragraph(filter_text + ", ".join(filter_parts), styles['FilterStyle']))
            story.append(Spacer(1, 0.1 * inch))


    data_rows = report_data.get('data', [])

    if not data_rows:
        story.append(Paragraph("Nenhum dado encontrado para o relatório com os filtros selecionados.", styles['NormalStyle']))
    else:
        headers = []
        column_widths = []
        if report_data['title'] == "Relatório de Movimentações Financeiras de Clientes":
            headers = ['Tipo', 'Valor', 'Data/Hora', 'Descrição', 'Conta Origem', 'Conta Destino', 'Cliente Origem']
            column_widths = [0.8*inch, 0.9*inch, 1.3*inch, 1.6*inch, 1.0*inch, 1.0*inch, 1.2*inch]
        elif report_data['title'] == "Relatório de Solicitações de Abertura de Conta":
            headers = ['ID', 'Cliente', 'Tipo Conta', 'Solicitação', 'Status', 'Valor Inicial', 'Aprovador', 'Aprovação']
            column_widths = [0.4*inch, 1.5*inch, 0.9*inch, 1.2*inch, 0.7*inch, 0.8*inch, 1.2*inch, 1.2*inch]
        elif report_data['title'] == "Relatório de Solicitações de Empréstimo":
            headers = ['ID', 'Cliente', 'Conta', 'Valor Solicitado', 'Valor Total', 'Taxa Juros', 'Prazo', 'Status', 'Score Risco', 'Aprovador']
            column_widths = [0.4*inch, 1.2*inch, 0.8*inch, 1.0*inch, 1.0*inch, 0.7*inch, 0.5*inch, 0.6*inch, 0.6*inch, 1.0*inch]
        elif report_data['title'] == "Relatório de Status e Ativação/Desativação de Funcionários":
            headers = ['ID', 'Nome', 'Cód. Func.', 'Cargo', 'Nível', 'Status', 'Agência']
            column_widths = [0.4*inch, 1.6*inch, 0.8*inch, 0.9*inch, 0.5*inch, 0.7*inch, 1.2*inch]
        elif report_data['title'] == "Relatório de Auditoria Geral do Sistema":
            headers = ['ID', 'Ação', 'Data/Hora', 'Detalhes', 'Usuário']
            column_widths = [0.4*inch, 1.2*inch, 1.3*inch, 2.5*inch, 1.5*inch]
        else:
            headers = list(data_rows[0].keys())
            col_width = (letter[0] - 2 * inch) / len(headers)
            column_widths = [col_width] * len(headers)


        table_data = [
            [Paragraph(header, styles['HeaderStyle']) for header in headers]
        ]
        
        for row_dict in data_rows:
            row_list = []
            for header_key in headers:
              
                if header_key == 'ID':
                    col_value = row_dict.get('id_solicitacao') or row_dict.get('id_emprestimo') or row_dict.get('id_funcionario') or row_dict.get('id_auditoria')
                elif header_key == 'Tipo':
                    col_value = row_dict.get('tipo')
                elif header_key == 'Valor':
                    col_value = row_dict.get('valor')
                elif header_key == 'Data/Hora':
                    col_value = row_dict.get('data_hora')
                elif header_key == 'Descrição':
                    col_value = row_dict.get('descricao')
                elif header_key == 'Conta Origem':
                    col_value = row_dict.get('conta_origem')
                elif header_key == 'Conta Destino':
                    col_value = row_dict.get('conta_destino')
                elif header_key == 'Cliente Origem':
                    col_value = row_dict.get('cliente_origem')
                elif header_key == 'Cliente':
                    col_value = row_dict.get('cliente')
                elif header_key == 'Tipo Conta':
                    col_value = row_dict.get('tipo_conta')
                elif header_key == 'Solicitação':
                    col_value = row_dict.get('data_solicitacao')
                elif header_key == 'Status':
                    col_value = row_dict.get('status')
                elif header_key == 'Valor Inicial':
                    col_value = row_dict.get('valor_inicial')
                elif header_key == 'Aprovador':
                    col_value = row_dict.get('funcionario_aprovador') or row_dict.get('aprovador_codigo')
                elif header_key == 'Aprovação':
                    col_value = row_dict.get('data_aprovacao')
                elif header_key == 'Conta':
                    col_value = row_dict.get('conta_cliente')
                elif header_key == 'Valor Solicitado':
                    col_value = row_dict.get('valor_solicitado')
                elif header_key == 'Valor Total':
                    col_value = row_dict.get('valor_total')
                elif header_key == 'Taxa Juros':
                    col_value = row_dict.get('taxa_juros')
                elif header_key == 'Prazo':
                    col_value = row_dict.get('prazo_meses')
                elif header_key == 'Score Risco':
                    col_value = row_dict.get('score_risco')
                elif header_key == 'Nome':
                    col_value = row_dict.get('nome')
                elif header_key == 'Cód. Func.':
                    col_value = row_dict.get('codigo_funcionario')
                elif header_key == 'Cargo':
                    col_value = row_dict.get('cargo')
                elif header_key == 'Nível':
                    col_value = row_dict.get('nivel_hierarquico')
                elif header_key == 'Agência':
                    col_value = row_dict.get('agencia')
                elif header_key == 'Ação':
                    col_value = row_dict.get('acao')
                elif header_key == 'Detalhes':
                    col_value = row_dict.get('detalhes')
                elif header_key == 'Usuário':
                    col_value = row_dict.get('usuario')
                else:
                    col_value = row_dict.get(header_key.lower().replace(' ', '_'), 'N/A')
                
                if header_key in ['Valor', 'Valor Solicitado', 'Valor Total', 'Taxa Juros', 'Score Risco', 'Valor Inicial']:
                    row_list.append(Paragraph(str(col_value), styles['ValueStyle']))
                elif header_key == 'ID':
                    row_list.append(Paragraph(str(col_value), styles['DataStyle']))
                else:
                    row_list.append(Paragraph(str(col_value), styles['DataStyle']))
            table_data.append(row_list)


        table = Table(table_data, colWidths=column_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#EEEEEE'),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0,0), (-1,-1), True),
        ]))
        story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer
