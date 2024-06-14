from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    crm = Column(String(50), nullable=False)
    specialty = Column(String(255), nullable=False)
