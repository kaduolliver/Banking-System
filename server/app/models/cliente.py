from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.db import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)
    score_credito = Column(Numeric(5, 2))

    usuario = relationship("Usuario", back_populates="cliente", uselist=False)
    contas = relationship("Conta", back_populates="cliente")
    emprestimos = relationship("Emprestimo", back_populates="cliente")

