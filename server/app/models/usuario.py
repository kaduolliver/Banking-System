from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from app.models.endereco import Endereco  

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    tipo_usuario = Column(String(50), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    otp_ativo = Column(Boolean, default=False)
    otp_codigo = Column(String(6))
    otp_expiracao = Column(TIMESTAMP)
    tentativas_login_falhas = Column(Integer, default=0, nullable=False)
    data_bloqueio = Column(DateTime, nullable=True)

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    funcionario = relationship("Funcionario", back_populates="usuario", uselist=False)
    endereco = relationship("Endereco", back_populates="usuario", uselist=False)
    auditorias = relationship("Auditoria", back_populates="usuario")


    __table_args__ = (
        CheckConstraint("tipo_usuario IN ('cliente', 'funcionario')", name='check_tipo_usuario'),
    )
