from sqlalchemy import Column, Integer, ForeignKey, Numeric, TIMESTAMP, String, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime, timezone

class Emprestimo(Base):
    __tablename__ = 'emprestimo'

    id_emprestimo = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_conta = Column(Integer, ForeignKey('conta.id_conta'), nullable=False)
    valor_solicitado = Column(Numeric(15, 2), nullable=False)
    taxa_juros_mensal = Column(Numeric(5, 2), nullable=False)
    prazo_meses = Column(Integer, nullable=False)
    valor_total = Column(Numeric(15, 2), nullable=False)
    data_solicitacao = Column(TIMESTAMP, nullable=False, default=lambda: datetime.now(timezone.utc))
    data_aprovacao = Column(TIMESTAMP)
    status = Column(String(20), nullable=False, default='PENDENTE')
    score_risco = Column(Numeric(5, 2))
    finalidade = Column(String(100), nullable=False) 

    cliente = relationship("Cliente", back_populates="emprestimos")
    conta = relationship("Conta", back_populates="emprestimos")

    __table_args__ = (
        CheckConstraint("prazo_meses BETWEEN 6 AND 60", name='check_prazo_meses'),
        CheckConstraint("status IN ('PENDENTE', 'APROVADO', 'REJEITADO', 'PAGO')", name='check_status_emprestimo'),
    )
