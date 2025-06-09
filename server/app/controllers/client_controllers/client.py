from app.services.client_services.solicitacao import solicitar_abertura_conta, verificar_possui_conta 

def cliente_solicitar_abertura_conta(data):
    return solicitar_abertura_conta(data)

def cliente_verificar_possui_conta(_):
    return verificar_possui_conta(_)