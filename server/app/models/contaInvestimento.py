from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.db import Base

class ContaInvestimento(Base):
    __tablename__ = 'conta_investimento'

    id_conta_investimento = Column(Integer, primary_key=True)
    id_conta = Column(Integer, ForeignKey('conta.id_conta'), unique=True, nullable=False)
    perfil_risco = Column(String(50), nullable=False)
    valor_minimo = Column(Numeric(15, 2), nullable=False, default=0.00)
    taxa_rendimento_base = Column(Numeric(5, 4), nullable=False)

    conta = relationship("Conta", back_populates="investimento")

    __table_args__ = (
        CheckConstraint(
            "perfil_risco IN ('conservador', 'moderado', 'arrojado')",
            name='check_perfil_risco'
        ),
    )
