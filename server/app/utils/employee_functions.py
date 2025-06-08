def gerar_codigo_estagiario(db):
    from app.models.funcionario import Funcionario

    ultimo_func = (
        db.query(Funcionario)
        .filter(Funcionario.cargo == "Estagiário")
        .order_by(Funcionario.codigo_funcionario.desc())
        .first()
    )
    if not ultimo_func:
        return "EST001"

    ultimo_codigo = ultimo_func.codigo_funcionario
    try:
        numero = int(ultimo_codigo[3:])
    except ValueError:
        numero = 0
    novo_numero = numero + 1
    return f"EST{novo_numero:03d}"
