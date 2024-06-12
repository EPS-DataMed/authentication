from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import userModel
from ..schemas import userSchema
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["usuarios"],
)

@router.post("/", response_model=userSchema.Usuario)
def create_usuario(usuario: userSchema.UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = db.query(userModel.Usuario).filter(userModel.Usuario.email == usuario.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(usuario.password)

    db_usuario = userModel.Usuario(
        full_name=usuario.full_name,
        email=usuario.email,
        password=hashed_password,
        birth_date=usuario.birth_date,
        biological_sex=usuario.biological_sex,
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario