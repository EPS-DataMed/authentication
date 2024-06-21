from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Doctor(Base):
    __tablename__ = "Doctors"

    user_id = Column(Integer, ForeignKey("Users.id"), primary_key=True)
    crm = Column(String(50), nullable=False)
    specialty = Column(String(255), nullable=False)

    user = relationship("User", back_populates="doctors")
