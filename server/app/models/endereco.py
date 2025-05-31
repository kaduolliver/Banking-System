from sqlalchemy import Column, Integer, String, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.database.db import Base

class Endereco(Base):
    __tablename__ = 'endereco'

    id_endereco = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero_casa = Column(String(255), nullable=False)
    bairro = Column(String(100), nullable=False)
    estado = Column(CHAR(2), nullable=False)
    complemento = Column(String(255))

    usuario = relationship("Usuario", back_populates="enderecos")
    agencia = relationship("Agencia", back_populates="endereco", uselist=False)
