from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base

class Funcionario(Base):
    __tablename__ = 'funcionario'

    id_funcionario = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)
    codigo_funcionario = Column(String(50), unique=True, nullable=False)
    cargo = Column(String(100), nullable=False)
    id_supervisor = Column(Integer, ForeignKey('funcionario.id_funcionario'))
    nivel_hierarquico = Column(Integer)
    id_agencia = Column(Integer, ForeignKey('agencia.id_agencia'), nullable=False)
    inativo = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="funcionario", uselist=False)
    supervisor = relationship("Funcionario", remote_side=[id_funcionario], backref="subordinados")
    relatorios = relationship("Relatorio", back_populates="funcionario")
    solicitacoes_aprovadas = relationship("SolicitacaoConta", back_populates="funcionario_aprovador")
    agencia = relationship("Agencia", back_populates="funcionarios")
