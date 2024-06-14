from sqlalchemy import JSON, CheckConstraint, Column, Date, DateTime, Integer,String
from sqlalchemy.sql import func

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    biological_sex = Column(String(1), CheckConstraint("biological_sex IN ('M', 'F')"), nullable=False)
    creation_date = Column(DateTime, default=func.now())