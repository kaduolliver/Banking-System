from sqlalchemy import Column, Integer, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime

class Relatorio(Base):
    __tablename__ = 'relatorio'

    id_relatorio = Column(Integer, primary_key=True)
    id_funcionario = Column(Integer, ForeignKey('funcionario.id_funcionario'), nullable=False)
    tipo_relatorio = Column(String(100), nullable=False)
    data_geracao = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    conteudo = Column(Text)

    funcionario = relationship("Funcionario", back_populates="relatorios")
