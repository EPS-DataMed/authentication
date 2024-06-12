from sqlalchemy import JSON, CheckConstraint, Column, Date, DateTime, Integer,String
from sqlalchemy.sql import func

from ..database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo_biologico = Column(String(1), CheckConstraint("sexo_biologico IN ('M', 'F')"), nullable=False)
    data_criacao = Column(DateTime, default=func.now())