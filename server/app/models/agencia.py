from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Agencia(Base):
    __tablename__ = 'agencia'

    id_agencia = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    codigo_agencia = Column(String(50), unique=True, nullable=False)
    endereco_id = Column(Integer, ForeignKey('endereco.id_endereco'), unique=True, nullable=False)

    endereco = relationship("Endereco", back_populates="agencia")
    contas = relationship("Conta", back_populates="agencia")
