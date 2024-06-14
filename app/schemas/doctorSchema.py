from pydantic import BaseModel, Field

class DoctorBase(BaseModel):
    crm: str = Field(..., max_length=50)
    specialty: str = Field(..., max_length=255)

class DoctorCreate(DoctorBase):
    user_id: int

class Doctor(DoctorBase):
    user_id: int

    class Config:
        orm_mode = True
