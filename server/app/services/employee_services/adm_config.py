from app.database.db import SessionLocal
from app.models.funcionario import Funcionario
from app.models.usuario import Usuario

def listar_funcionarios():
    db = SessionLocal()
    try:
        funcionarios = (
            db.query(
                Funcionario.id_funcionario.label("id"),
                Usuario.nome,
                Funcionario.cargo,
                Funcionario.codigo_funcionario,
                Funcionario.inativo
            )
            .join(Usuario)
            .filter(Funcionario.cargo != 'Admin')
            .all()
        )

        resultado = []
        for f in funcionarios:
            resultado.append({
                "id": f.id,
                "nome": f.nome,
                "cargo": f.cargo,
                "codigo_funcionario": f.codigo_funcionario,
                "inativo": f.inativo
            })

        return resultado
    finally:
        db.close()

def atualizar_status_funcionario(id_funcionario: int, novo_status: bool):
    db = SessionLocal()
    try:
        funcionario = db.query(Funcionario).filter_by(id_funcionario=id_funcionario).first()
        if not funcionario:
            return {"erro": "Funcionário não encontrado."}, 404

        funcionario.inativo = novo_status
        db.commit()
        return {"mensagem": "Status atualizado com sucesso."}, 200
    finally:
        db.close()
