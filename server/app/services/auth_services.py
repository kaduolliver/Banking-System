from app.database.db import SessionLocal
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.agencia import Agencia
from app.models.conta import Conta
from app.utils.security import hash_senha, gerar_otp, verificar_senha
from app.utils.validators import validar_data, validar_campos_obrigatorios, validar_cpf
from app.utils.employee_functions import gerar_codigo_estagiario
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from flask import session
from sqlalchemy.orm import joinedload, subqueryload
from app.utils.user_helper import montar_dados_usuario
from sqlalchemy import text

# Funcionamento de um .joinedload

# Usuario
# ├── Funcionario
# │   └── Agencia
# └── Cliente
#     ├── Emprestimos
#     └── Contas
#         ├── Agencia
#         ├── Corrente
#         ├── Poupanca
#         └── Investimento

MAX_TENTATIVAS_LOGIN = 3
TEMPO_BLOQUEIO_MINUTOS = 5

def registrar_usuario(data):
    db = SessionLocal()
    try:
        obrigatorios = ['nome', 'cpf', 'data_nascimento', 'telefone', 'tipo_usuario', 'senha']
        ok, msg = validar_campos_obrigatorios(data, obrigatorios)
        if not ok:
            return {"erro": msg}, 400

        nome = data['nome']
        cpf = data['cpf']
        tipo = data['tipo_usuario']
        senha = data['senha']
        telefone = data['telefone'] 

        if tipo not in ['cliente', 'funcionario']:
            return {"erro": "Tipo de usuário inválido"}, 400

        if not validar_cpf(cpf):
            return {"erro": "CPF inválido. Deve conter 11 dígitos numéricos."}, 400

        nascimento = validar_data(data['data_nascimento'])
        if not nascimento:
            return {"erro": "Data de nascimento inválida. Use o formato YYYY-MM-DD."}, 400

        senha_hash = hash_senha(senha)

        novo_usuario = Usuario(
            nome=nome,
            cpf=cpf,
            data_nascimento=nascimento,
            telefone=telefone,
            tipo_usuario=tipo,
            senha_hash=senha_hash
        )

        db.add(novo_usuario)
        db.flush() 

        if tipo == 'cliente':
            db.add(Cliente(id_usuario=novo_usuario.id_usuario))
        else: 
            
            id_agencia = data.get('id_agencia')

            
            if id_agencia is None:
                
                return {"erro": "Para tipo 'funcionario', 'id_agencia' é obrigatório."}, 400
            
            agencia_existente = db.query(Agencia).filter_by(id_agencia=id_agencia).first()
            if not agencia_existente:
                return {"erro": f"Agência com ID {id_agencia} não encontrada."}, 400

            codigo_gerado = gerar_codigo_estagiario(db)
            db.add(Funcionario(
                id_usuario=novo_usuario.id_usuario,
                codigo_funcionario=codigo_gerado,
                cargo="Estagiário", 
                id_supervisor=None,
                id_agencia=id_agencia,
                nivel_hierarquico=1,
            ))

        db.commit()
        return {"mensagem": "Usuário registrado com sucesso!"}, 200

    except IntegrityError as e:
        db.rollback()
        
        if "cpf" in str(e).lower():
            return {"erro": "CPF já registrado."}, 400
        return {"erro": "Erro de integridade do banco de dados: " + str(e)}, 500
    except Exception as e:
        db.rollback()
        return {"erro": str(e)}, 500
    finally:
        db.close()


def login_usuario(data):
    db = SessionLocal()
    try:
        obrigatorios = ['cpf', 'senha']
        ok, msg = validar_campos_obrigatorios(data, obrigatorios)
        if not ok:
            return {'erro': msg}, 400

        usuario = db.query(Usuario).options(
            joinedload(Usuario.funcionario).joinedload(Funcionario.agencia)
        ).filter_by(cpf=data['cpf']).first()

        if not usuario:
            try:
                db.execute(text("SELECT fn_registrar_auditoria(NULL, :acao, :detalhes);"),
                           {"acao": "TENTATIVA_LOGIN_CPF_INEXISTENTE",
                            "detalhes": f"Tentativa de login para CPF inexistente: {data['cpf']}"})
                db.commit()
            except Exception as audit_e:
                print(f"Erro ao registrar auditoria de CPF inexistente: {audit_e}")
            return {'erro': 'CPF ou senha inválidos.'}, 401

        if usuario.data_bloqueio:
            
            if datetime.now() < (usuario.data_bloqueio + timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS)):
                
                return {'erro': f'Sua conta está temporariamente bloqueada. Tente novamente em {TEMPO_BLOQUEIO_MINUTOS} minutos.'}, 403
            else:
                
                usuario.tentativas_login_falhas = 0
                usuario.data_bloqueio = None
                db.commit() 

                try:
                    db.execute(text("SELECT fn_registrar_auditoria(:user_id, :acao, :detalhes);"),
                               {"user_id": usuario.id_usuario,
                                "acao": "CONTA_DESBLOQUEADA_AUTOMATICAMENTE",
                                "detalhes": f"Conta ID {usuario.id_usuario} desbloqueada automaticamente após {TEMPO_BLOQUEIO_MINUTOS} minutos."})
                    db.commit() 
                except Exception as audit_e:
                    print(f"Erro ao registrar desbloqueio automático na auditoria: {audit_e}")
                    db.rollback() 

        
        if not verificar_senha(data['senha'], usuario.senha_hash):
            usuario.tentativas_login_falhas += 1
            db.commit() 

            try:
                db.execute(text("SELECT fn_registrar_auditoria(:user_id, :acao, :detalhes);"),
                           {"user_id": usuario.id_usuario,
                            "acao": "FALHA_LOGIN_SENHA_INCORRETA",
                            "detalhes": f"Tentativa de login falhou para CPF {usuario.cpf}. Tentativa {usuario.tentativas_login_falhas} de {MAX_TENTATIVAS_LOGIN}."})
                db.commit() 
            except Exception as audit_e:
                print(f"Erro ao registrar falha de login na auditoria para o usuário {usuario.id_usuario}: {audit_e}")
                db.rollback() 

            
            if usuario.tentativas_login_falhas >= MAX_TENTATIVAS_LOGIN:
                usuario.data_bloqueio = datetime.now()
                db.commit() 

                try:
                    db.execute(text("SELECT fn_registrar_auditoria(:user_id, :acao, :detalhes);"),
                               {"user_id": usuario.id_usuario,
                                "acao": "CONTA_BLOQUEADA_TENTATIVAS",
                                "detalhes": f"Conta ID {usuario.id_usuario} bloqueada após {MAX_TENTATIVAS_LOGIN} tentativas de senha inválidas."})
                    db.commit() 
                except Exception as audit_e:
                    print(f"Erro ao registrar bloqueio de conta na auditoria para o usuário {usuario.id_usuario}: {audit_e}")
                    db.rollback() 

                return {'erro': f'CPF ou senha inválidos. Sua conta foi bloqueada por {TEMPO_BLOQUEIO_MINUTOS} minutos.'}, 401
            else:
            
                return {'erro': f'CPF ou senha inválidos. Você tem mais {MAX_TENTATIVAS_LOGIN - usuario.tentativas_login_falhas} tentativas antes que sua conta seja bloqueada.'}, 401

        usuario.tentativas_login_falhas = 0
        usuario.data_bloqueio = None

        otp = gerar_otp()
        expiracao = datetime.now() + timedelta(minutes=5)

        usuario.otp_codigo = otp
        usuario.otp_expiracao = expiracao
        usuario.otp_ativo = True

        db.commit()

        print(f"OTP para {usuario.cpf}: {otp}")

        dados_usuario = montar_dados_usuario(usuario)
        endereco = dados_usuario.pop('endereco_agencia', None)

        return {
            'mensagem': 'OTP enviado para validação.',
            'precisa_otp': True,
            'endereco_agencia': endereco,
            **dados_usuario
        }, 200

    
    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


def validar_otp(data):
    db = SessionLocal()
    try:
        ok, msg = validar_campos_obrigatorios(data, ['cpf', 'otp'])
        if not ok:
            return {'erro': msg}, 400

        usuario = db.query(Usuario).options(
            joinedload(Usuario.funcionario).joinedload(Funcionario.agencia),
            joinedload(Usuario.cliente)
                .joinedload(Cliente.emprestimos), 
            joinedload(Usuario.cliente)
                .joinedload(Cliente.contas)
                .joinedload(Conta.agencia),
            joinedload(Usuario.cliente)
                .joinedload(Cliente.contas)
                .joinedload(Conta.corrente),
            joinedload(Usuario.cliente)
                .joinedload(Cliente.contas)
                .joinedload(Conta.poupanca),
            joinedload(Usuario.cliente)
                .joinedload(Cliente.contas)
                .joinedload(Conta.investimento)
        ).filter_by(cpf=data['cpf'], otp_ativo=True).first()


        if not usuario or usuario.otp_codigo != data['otp']:
            return {'erro': 'OTP inválido ou não encontrado.'}, 400

        if datetime.now() > usuario.otp_expiracao:
            return {'erro': 'OTP expirado.'}, 400

        usuario.otp_codigo = None
        usuario.otp_expiracao = None
        usuario.otp_ativo = False

        session['id_usuario'] = usuario.id_usuario
        session['tipo'] = usuario.tipo_usuario
        if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
            session['id_funcionario'] = usuario.funcionario.id_funcionario
            session['cargo'] = usuario.funcionario.cargo

        db.commit()

        try:
            db.execute(text("SELECT fn_registrar_auditoria(:user_id, :acao, :detalhes);"),
                       {"user_id": usuario.id_usuario,
                        "acao": "LOGIN_SUCESSO", 
                        "detalhes": f"Usuário {usuario.nome} ({usuario.tipo_usuario}) realizou login com sucesso após OTP."})
            db.commit() 
        except Exception as audit_e:
            print(f"Erro ao registrar login de sucesso na auditoria para o usuário {usuario.id_usuario}: {audit_e}")
            db.rollback() 

        dados_usuario = montar_dados_usuario(usuario)

        if usuario.tipo_usuario == 'funcionario' and usuario.funcionario:
            if usuario.funcionario.agencia:
                session['id_agencia'] = usuario.funcionario.agencia.id_agencia


        return {
            'mensagem': 'Login completo!',
            **dados_usuario
        }, 200

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()

def logout_usuario():
    db = SessionLocal()
    try:
        user_id = session.get('id_usuario')
        if not user_id:
            return {'erro': 'Nenhum usuário logado na sessão.'}, 400

        usuario = db.query(Usuario).filter_by(id_usuario=user_id).first()
        if usuario:
            usuario.otp_codigo = None
            usuario.otp_expiracao = None
            usuario.otp_ativo = False
            db.commit()

        try:
            db.execute(text("SELECT fn_registrar_logout(:user_id);"), {"user_id": user_id})
            db.commit() 
        except Exception as audit_e:
            print(f"Erro ao registrar logout na auditoria para o usuário {user_id}: {audit_e}")
            db.rollback() 

        session.clear() 
        return {'mensagem': 'Logout realizado com sucesso.'}, 200

    except Exception as e:
        db.rollback()
        return {'erro': str(e)}, 500
    finally:
        db.close()


def verificar_sessao():
    if 'id_usuario' not in session:
        return {'autenticado': False}, 401

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).options(
            joinedload(Usuario.funcionario).joinedload(Funcionario.agencia),
            joinedload(Usuario.cliente)
                .joinedload(Cliente.emprestimos), 
            joinedload(Usuario.cliente)
                .joinedload(Cliente.contas)
                .joinedload(Conta.agencia)
        ).filter_by(id_usuario=session['id_usuario']).first()

        if not usuario:
            return {'erro': 'Usuário não encontrado'}, 404

        dados_usuario = montar_dados_usuario(usuario)

        return {
            'autenticado': True,
            'usuario': dados_usuario
        }, 200

    finally:
        db.close()
        

def obter_usuario_atual(id_usuario: int):
    
    db = SessionLocal()
    try:
        usuario = (
            db.query(Usuario)
              .options(
                  joinedload(Usuario.funcionario).joinedload(Funcionario.agencia),
                  joinedload(Usuario.cliente)
                      .joinedload(Cliente.emprestimos),
                  joinedload(Usuario.cliente)
                      .joinedload(Cliente.contas)
                      .joinedload(Conta.agencia),
                  joinedload(Usuario.cliente)
                      .joinedload(Cliente.contas)
                      .joinedload(Conta.corrente),
                  joinedload(Usuario.cliente)
                      .joinedload(Cliente.contas)
                      .joinedload(Conta.poupanca),
                  joinedload(Usuario.cliente)
                      .joinedload(Cliente.contas)
                      .joinedload(Conta.investimento),
              )
              .filter_by(id_usuario=id_usuario)
              .first()
        )
        if not usuario:
            raise LookupError("Usuário não encontrado")

        return montar_dados_usuario(usuario)
    finally:
        db.close()

