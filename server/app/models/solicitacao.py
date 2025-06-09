from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime, timezone

class SolicitacaoConta(Base):
    __tablename__ = 'solicitacao_conta'

    id_solicitacao = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    tipo_conta = Column(String(50), nullable=False)
    data_solicitacao = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), nullable=False, default='PENDENTE')
    id_funcionario_aprovador = Column(Integer, ForeignKey('funcionario.id_funcionario'), nullable=True)
    observacoes = Column(String(500))
    valor_inicial = Column(Numeric(15, 2), default=0.00)
    data_aprovacao = Column(DateTime, default=None)

    cliente = relationship("Cliente", back_populates="solicitacoes_conta")
    funcionario_aprovador = relationship("Funcionario", back_populates="solicitacoes_aprovadas")

    __table_args__ = (
        CheckConstraint("tipo_conta IN ('corrente', 'poupanca', 'investimento')", name='check_tipo_conta_solicitada'),
        CheckConstraint("status IN ('PENDENTE', 'APROVADA', 'REJEITADA')", name='check_status_solicitacao'),
    )
