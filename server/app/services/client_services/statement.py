from sqlalchemy.orm import Session, aliased 
from sqlalchemy import or_, desc, func
from app.database.db import SessionLocal
from app.models.cliente import Cliente
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.models.emprestimo import Emprestimo
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import black
import io

def obter_extrato_cliente(id_usuario: int, start_date: str = None, end_date: str = None, limit: int = 10):

    db: Session = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id_usuario=id_usuario).first()
        if not cliente:
            raise LookupError("Cliente não encontrado.")

        id_cliente = cliente.id_cliente
        operacoes = []

        data_inicio_dt = None
        data_fim_dt = None
        if start_date:
            try:
                data_inicio_dt = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Formato de data de início inválido. Use YYYY-MM-DD.")
        if end_date:
            try:
                data_fim_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            except ValueError:
                raise ValueError("Formato de data de fim inválido. Use YYYY-MM-DD.")

        ContaOrigem = aliased(Conta)
        ContaDestino = aliased(Conta)

        transacoes_query = db.query(
            Transacao.tipo_transacao,
            Transacao.valor,
            Transacao.data_hora,
            Transacao.descricao,
            ContaOrigem.numero_conta.label('conta_origem_numero'),
            func.coalesce(ContaDestino.numero_conta, 'N/A').label('conta_destino_numero')
        ).join(
            ContaOrigem, Transacao.id_conta_origem == ContaOrigem.id_conta
        ).outerjoin(
            ContaDestino, Transacao.id_conta_destino == ContaDestino.id_conta
        ).filter(
            or_(ContaOrigem.id_cliente == id_cliente, ContaDestino.id_cliente == id_cliente)
        )

        if data_inicio_dt:
            transacoes_query = transacoes_query.filter(Transacao.data_hora >= data_inicio_dt)
        if data_fim_dt:
            transacoes_query = transacoes_query.filter(Transacao.data_hora <= data_fim_dt)

        transacoes_result = transacoes_query.order_by(desc(Transacao.data_hora)).limit(limit).all()

        for t in transacoes_result:
            operacao_tipo = t.tipo_transacao
            valor_formatado = f"R$ {t.valor:.2f}"

            if t.tipo_transacao == 'deposito':
                operacao_tipo = 'Depósito'
                valor_formatado = f"+ R$ {t.valor:.2f}"
            elif t.tipo_transacao == 'saque':
                operacao_tipo = 'Saque'
                valor_formatado = f"- R$ {t.valor:.2f}"
            elif t.tipo_transacao == 'transferencia':
                cliente_contas_numeros = [c.numero_conta for c in db.query(Conta.numero_conta).filter_by(id_cliente=id_cliente).all()]

                if t.conta_origem_numero in cliente_contas_numeros:
                    operacao_tipo = 'Transferência Enviada'
                    valor_formatado = f"- R$ {t.valor:.2f}"
                elif t.conta_destino_numero in cliente_contas_numeros and t.conta_origem_numero != 'N/A':
                    operacao_tipo = 'Transferência Recebida'
                    valor_formatado = f"+ R$ {t.valor:.2f}"
                else:
                    operacao_tipo = 'Transferência'
                    valor_formatado = f"R$ {t.valor:.2f}"


            operacoes.append({
                "tipo": operacao_tipo,
                "valor": valor_formatado,
                "data_hora": t.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
                "descricao": t.descricao or "N/A",
                "conta_origem": t.conta_origem_numero,
                "conta_destino": t.conta_destino_numero if t.conta_destino_numero != 'N/A' else ''
            })

        emprestimos_query = db.query(
            Emprestimo.valor_solicitado,
            Emprestimo.data_solicitacao,
            Emprestimo.status,
            Emprestimo.finalidade,
            Emprestimo.valor_total,
            Conta.numero_conta.label('conta_associada_numero')
        ).join(
            Conta, Emprestimo.id_conta == Conta.id_conta
        ).filter(
            Emprestimo.id_cliente == id_cliente
        )

        if data_inicio_dt:
            emprestimos_query = emprestimos_query.filter(Emprestimo.data_solicitacao >= data_inicio_dt)
        if data_fim_dt:
            emprestimos_query = emprestimos_query.filter(Emprestimo.data_solicitacao <= data_fim_dt)

        emprestimos_result = emprestimos_query.order_by(desc(Emprestimo.data_solicitacao)).limit(limit).all()

        for e in emprestimos_result:
            operacoes.append({
                "tipo": f"Empréstimo ({e.status})",
                "valor": f"R$ {e.valor_solicitado:.2f} (Total: R$ {e.valor_total:.2f})",
                "data_hora": e.data_solicitacao.strftime('%Y-%m-%d %H:%M:%S'),
                "descricao": f"Finalidade: {e.finalidade}",
                "conta_origem": "N/A",
                "conta_destino": e.conta_associada_numero
            })

        for op in operacoes:
            if isinstance(op['data_hora'], str):
                op['data_hora_sortable'] = datetime.strptime(op['data_hora'], '%Y-%m-%d %H:%M:%S')
            else:
                op['data_hora_sortable'] = op['data_hora'] 

        operacoes_ordenadas = sorted(operacoes, key=lambda x: x['data_hora_sortable'], reverse=True)

        return operacoes_ordenadas[:limit]

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def gerar_pdf_extrato(extrato_data: list, id_usuario: int):
   
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='TitleStyle',
                               fontSize=20,
                               leading=24,
                               alignment=TA_CENTER,
                               spaceAfter=20,
                               fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SubtitleStyle',
                               fontSize=14,
                               leading=16,
                               alignment=TA_CENTER,
                               spaceAfter=10,
                               fontName='Helvetica'))
    styles.add(ParagraphStyle(name='NormalStyle',
                               fontSize=10,
                               leading=12,
                               alignment=TA_LEFT,
                               spaceAfter=5,
                               fontName='Helvetica'))
    styles.add(ParagraphStyle(name='HeaderStyle',
                               fontSize=10,
                               leading=12,
                               alignment=TA_CENTER,
                               fontName='Helvetica-Bold',
                               textColor=black))
    styles.add(ParagraphStyle(name='DataStyle',
                               fontSize=10,
                               leading=12,
                               alignment=TA_LEFT,
                               fontName='Helvetica'))
    styles.add(ParagraphStyle(name='ValueStyle',
                               fontSize=10,
                               leading=12,
                               alignment=TA_RIGHT,
                               fontName='Helvetica'))


    story = []

    story.append(Paragraph(f"Extrato Financeiro do Cliente", styles['TitleStyle']))
    story.append(Paragraph(f"ID do Cliente: {id_usuario}", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.2 * inch))

    if not extrato_data:
        story.append(Paragraph("Nenhuma operação encontrada para o período selecionado.", styles['NormalStyle']))
    else:
        data = [['Tipo', 'Valor', 'Data/Hora', 'Descrição', 'Conta Origem', 'Conta Destino']]
        for op in extrato_data:
            data.append([
                Paragraph(str(op.get('tipo', 'N/A')), styles['DataStyle']),
                Paragraph(str(op.get('valor', 'N/A')), styles['ValueStyle']),
                Paragraph(str(op.get('data_hora', 'N/A')), styles['DataStyle']),
                Paragraph(str(op.get('descricao', 'N/A')), styles['DataStyle']),
                Paragraph(str(op.get('conta_origem', 'N/A')), styles['DataStyle']),
                Paragraph(str(op.get('conta_destino', 'N/A')), styles['DataStyle']),
            ])

        table = Table(data, colWidths=[1.2*inch, 1.2*inch, 1.4*inch, 2.0*inch, 1.0*inch, 1.0*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#EEEEEE'), 
            ('TEXTCOLOR', (0, 0), (-1, 0), black),      
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),        
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),          
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),      
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer
