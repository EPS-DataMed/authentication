from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import userModel
from ..schemas import userSchema
from ..utils import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Usuarios"],
)

@router.post("/users", response_model=userSchema.User)
def create_user(User: userSchema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(userModel.User).filter(userModel.User.email == User.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(User.password)

    db_User = userModel.User(
        full_name=User.full_name,
        email=User.email,
        password=hashed_password,
        birth_date=User.birth_date,
        biological_sex=User.biological_sex,
    )

    db.add(db_User)
    db.commit()
    db.refresh(db_User)
    return db_User