from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.db import Base

class ContaPoupanca(Base):
    __tablename__ = 'conta_poupanca'

    id_conta_poupanca = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey('conta.id_conta'), unique=True, nullable=False)
    taxa_rendimento = Column(Numeric(5, 4), nullable=False)
    ultimo_rendimento = Column(Numeric(15, 2))

    conta = relationship("Conta", back_populates="poupanca")
