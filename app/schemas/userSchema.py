from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    birth_date: date
    biological_sex: str
    creation_date: datetime

class TokenData(BaseModel):
    user_id: int = None

class UserBase(BaseModel):
    full_name: str = Field(..., max_length=255)
    email: EmailStr
    birth_date: date
    biological_sex: str = Field(..., max_length=1, pattern='^(M|F)$')

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(UserBase):
    pass

class UserPasswordUpdate(BaseModel):
    password: str = Field(..., min_length=6)

class UserPasswordCompare(BaseModel):
    password: str = Field(..., min_length=6)

class User(BaseModel):
    id: int
    creation_date: datetime
    full_name: str
    email: EmailStr
    birth_date: date
    biological_sex: str
    password: str