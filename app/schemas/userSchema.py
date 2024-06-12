from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field

class UsuarioOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    birth_date: date
    biological_sex: str
    creation_date: datetime

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    user_id: int = None

class UsuarioBase(BaseModel):
    full_name: str = Field(..., max_length=255)
    email: EmailStr
    birth_date: date
    biological_sex: str = Field(..., max_length=1, pattern='^(M|F)$')

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioUpdate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    creation_date: datetime
    password: str

    class Config:
        orm_mode = True