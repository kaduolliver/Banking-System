from sqlalchemy import Column, Integer, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime

class Auditoria(Base):
    __tablename__ = 'auditoria'

    id_auditoria = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    acao = Column(String(100), nullable=False)
    data_hora = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    detalhes = Column(Text)

    usuario = relationship("Usuario", back_populates="auditorias")
