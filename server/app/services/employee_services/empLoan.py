from sqlalchemy import text
from sqlalchemy.orm import joinedload
from app.database.db import SessionLocal
from app.models.emprestimo import Emprestimo
from app.models.cliente import Cliente
from app.models.usuario import Usuario

def listar_emprestimos_pendentes():
    db = SessionLocal()
    try:
        emprestimos = (
            db.query(Emprestimo)
              .options(joinedload(Emprestimo.cliente).joinedload(Cliente.usuario))
              .filter(Emprestimo.status == 'PENDENTE')
              .order_by(Emprestimo.data_solicitacao.asc())
              .all()
        )

        resultado = []
        for emp in emprestimos:
            resultado.append({
                "id_emprestimo": emp.id_emprestimo,
                "cliente": emp.cliente.usuario.nome,
                "valor_solicitado": float(emp.valor_solicitado),
                "prazo_meses": emp.prazo_meses,
                "score_risco": float(emp.score_risco) if emp.score_risco else None,
                "finalidade": emp.finalidade,
                "data_solicitacao": emp.data_solicitacao.isoformat()
            })
        return resultado
    finally:
        db.close()

def decidir_emprestimo(id_emprestimo: int, aprovado: bool, id_funcionario: int):
   
    db = SessionLocal()
    try:
        result = db.execute(
            text("CALL decidir_emprestimo(:emp_id, :yes, :func)"),
            {"emp_id": id_emprestimo, "yes": aprovado, "func": id_funcionario}
        )
        db.commit()

        if result.rowcount == 0:
            raise ValueError("Empréstimo inexistente ou já decidido.")

        status_txt = "aprovado" if aprovado else "rejeitado"
        return {"mensagem": f"Empréstimo {id_emprestimo} {status_txt} com sucesso."}

    except ValueError:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise RuntimeError(str(e))
    finally:
        db.close()
