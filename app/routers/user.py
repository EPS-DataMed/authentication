from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import userModel
from ..schemas import userSchema
from .. import utils

router = APIRouter(
    prefix="/auth",
    tags=["Usuarios"],
)

@router.post("/users", response_model=userSchema.User)
def create_user(User: userSchema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(userModel.User).filter(userModel.User.email == User.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    encrypted_password = utils.encrypt_password(User.password)

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

@router.put("/users/{user_id}/password", response_model=userSchema.User)
def update_password(user_id: int, new_password: userSchema.UserPasswordUpdate, db: Session = Depends(get_db)):
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    encrypted_password = utils.encrypt_password(new_password.password)

    user.password = encrypted_password
    db.commit()
    db.refresh(user)

    return user

@router.post("/users/{user_id}/compare-password", response_model=bool)
def compare_password(user_id: int, password_data: userSchema.UserPasswordCompare, db: Session = Depends(get_db)):
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    decrypted_password = utils.decrypt_password(user.password)

    return decrypted_password == password_data.password
