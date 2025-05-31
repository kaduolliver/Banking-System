from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import date

class Conta(Base):
    __tablename__ = 'conta'

    id_conta = Column(Integer, primary_key=True)
    numero_conta = Column(String(20), unique=True, nullable=False)
    id_agencia = Column(Integer, ForeignKey('agencia.id_agencia'), nullable=False)
    saldo = Column(Numeric(15, 2), nullable=False, default=0.00)
    tipo_conta = Column(String(50), nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    data_abertura = Column(Date, nullable=False, default=date.today)
    status = Column(String(20), nullable=False, default='ativa')

    cliente = relationship("Cliente", back_populates="contas")
    agencia = relationship("Agencia", back_populates="contas")
    poupanca = relationship("ContaPoupanca", back_populates="conta", uselist=False)
    corrente = relationship("ContaCorrente", back_populates="conta", uselist=False)
    investimento = relationship("ContaInvestimento", back_populates="conta", uselist=False)
    transacoes_origem = relationship("Transacao", back_populates="conta_origem", foreign_keys='Transacao.id_conta_origem')
    transacoes_destino = relationship("Transacao", back_populates="conta_destino", foreign_keys='Transacao.id_conta_destino')
    emprestimos = relationship("Emprestimo", back_populates="conta")

    __table_args__ = (
        CheckConstraint("tipo_conta IN ('corrente', 'poupanca', 'investimento')", name='check_tipo_conta'),
    )