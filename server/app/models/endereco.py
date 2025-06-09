from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base

class Endereco(Base):
    __tablename__ = 'endereco'

    id_endereco = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=True)
    id_agencia = Column(Integer, ForeignKey('agencia.id_agencia'), unique=True, nullable=True)

    cep = Column(String(10), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero_casa = Column(String(255), nullable=False)
    bairro = Column(String(100), nullable=False)
    estado = Column(CHAR(2), nullable=False)
    complemento = Column(String(255))

    __table_args__ = (
        CheckConstraint(
            '((id_usuario IS NOT NULL AND id_agencia IS NULL) OR (id_usuario IS NULL AND id_agencia IS NOT NULL))',
            name='endereco_usuario_ou_agencia_ck'
        ),
    )

    usuario = relationship("Usuario", back_populates="endereco", uselist=False)
    agencia = relationship("Agencia", back_populates="endereco", uselist=False)
