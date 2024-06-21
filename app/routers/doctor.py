from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import doctorModel, userModel
from app.schemas import doctorSchema
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["medicos"]
)

@router.post("/doctors", response_model=doctorSchema.Doctor)
def create_doctor(doctor: doctorSchema.DoctorCreate, db: Session = Depends(get_db)):
    db_user = db.query(userModel.User).filter(userModel.User.id == doctor.user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Associated user not found")
    
    existing_doctor = db.query(doctorModel.Doctor).filter(doctorModel.Doctor.user_id == doctor.user_id).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Doctor already registered")
    
    db_doctor = doctorModel.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
