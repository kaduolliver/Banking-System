from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base

class Agencia(Base):
    __tablename__ = 'agencia'

    id_agencia = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    codigo_agencia = Column(String(50), unique=True, nullable=False)

    endereco = relationship("Endereco", back_populates="agencia", uselist=False)
    contas = relationship("Conta", back_populates="agencia")
