from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import os

from ..database import get_db
from ..models import userModel
from ..schemas import userSchema

router = APIRouter(
    prefix="/auth",
    tags=["Usuarios"],
)

def encrypt_password(password: str) -> str:
    url = os.getenv("URL_CYPHER")
    public_key = os.getenv("PUBLIC_KEY")
    data = {
        "message": password,
        "public_key": public_key,
    }
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error encrypting password")
    
    return response.json()["encrypted_message"]

@router.post("/users", response_model=userSchema.User)
def create_user(User: userSchema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(userModel.User).filter(userModel.User.email == User.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    encrypted_password = encrypt_password(User.password)

    db_User = userModel.User(
        full_name=User.full_name,
        email=User.email,
        password=encrypted_password,
        birth_date=User.birth_date,
        biological_sex=User.biological_sex,
    )

    db.add(db_User)
    db.commit()
    db.refresh(db_User)
    return db_User
