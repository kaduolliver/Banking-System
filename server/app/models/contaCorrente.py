from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from app.database.db import Base

class ContaCorrente(Base):
    __tablename__ = 'conta_corrente'

    id_conta_corrente = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey('conta.id_conta'), unique=True, nullable=False)
    limite = Column(Numeric(15, 2), nullable=False, default=0.00)
    data_vencimento = Column(Date)
    taxa_manutencao = Column(Numeric(5, 2), nullable=False, default=0.00)

    conta = relationship("Conta", back_populates="corrente")
