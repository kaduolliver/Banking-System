from app.services.agency_services.agency import get_endereco_agencia

def montar_dados_usuario(usuario):
    cargo = None
    id_funcionario = None
    id_agencia = None
    nome_agencia = None
    codigo_agencia = None
    endereco = None
    status_endereco = None

    if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
        cargo = usuario.funcionario.cargo
        id_funcionario = usuario.funcionario.id_funcionario
        if usuario.funcionario.agencia:
            id_agencia = usuario.funcionario.agencia.id_agencia
            nome_agencia = usuario.funcionario.agencia.nome
            codigo_agencia = usuario.funcionario.agencia.codigo_agencia
            endereco, status_endereco = get_endereco_agencia(id_agencia)
        else:
            endereco, status_endereco = None, None

    dados = {
        'id_usuario': usuario.id_usuario,
        'tipo_usuario': usuario.tipo_usuario,
        'nome': usuario.nome,
        'cpf': usuario.cpf,
        'data_nascimento': usuario.data_nascimento.isoformat(),
        'telefone': usuario.telefone,
        'cargo': cargo,
        'id_funcionario': id_funcionario,
        'id_agencia': id_agencia,
        'nome_agencia': nome_agencia,
        'codigo_agencia': codigo_agencia,
        'endereco_agencia': endereco if status_endereco == 200 else None
    }

    return dados
