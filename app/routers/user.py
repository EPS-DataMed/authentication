from ..schemas import userSchema
from ..models import userModel
from .. import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)

# Recuperar Usuario pelo ID
@router.get("/{usuario_id}", response_model=userSchema.UsuarioOut)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(userModel.Usuario).filter(userModel.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

# Recuperar todos os Usuarios
@router.get("/", response_model=list[userSchema.UsuarioOut])
def read_usuarios(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    usuarios = db.query(userModel.Usuario).all()
    return usuarios