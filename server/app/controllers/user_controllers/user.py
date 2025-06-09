from app.services.user_services.userData import add_endereco, get_endereco, atualizar_usuario

def user_add_endereco(data):
    return add_endereco(data)

def user_get_endereco():
    return get_endereco()

def user_atualizar_usuario(data):
    return atualizar_usuario(data)