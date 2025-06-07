from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime, timezone

class Transacao(Base):
    __tablename__ = 'transacao'

    id_transacao = Column(Integer, primary_key=True)
    id_conta_origem = Column(Integer, ForeignKey('conta.id_conta'), nullable=False)
    id_conta_destino = Column(Integer, ForeignKey('conta.id_conta'))
    tipo_transacao = Column(String(50), nullable=False)
    valor = Column(Numeric(15, 2), nullable=False)
    data_hora = Column(TIMESTAMP, nullable=False, default=lambda: datetime.now(timezone.utc))
    descricao = Column(Text)

    conta_origem = relationship("Conta", foreign_keys=[id_conta_origem], back_populates="transacoes_origem")
    conta_destino = relationship("Conta", foreign_keys=[id_conta_destino], back_populates="transacoes_destino")

    __table_args__ = (
        CheckConstraint(
            "tipo_transacao IN ('deposito', 'saque', 'transferencia')",
            name='check_tipo_transacao'
        ),
    )
