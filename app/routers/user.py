from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import oauth2
from ..database import get_db
from ..models import userModel
from ..schemas import userSchema
from ..utils import hash_password

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)

@router.get("/{usuario_id}", response_model=userSchema.UsuarioOut)
def read_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db_usuario = db.query(userModel.Usuario).filter(userModel.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@router.get("/", response_model=list[userSchema.UsuarioOut])
def read_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(userModel.Usuario).all()
    return usuarios

@router.post("/", response_model=userSchema.Usuario)
def create_usuario(usuario: userSchema.UsuarioCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    existing_user = db.query(userModel.Usuario).filter(userModel.Usuario.email == usuario.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(usuario.senha)
    db_usuario = userModel.Usuario(
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        senha=hashed_password,
        data_nascimento=usuario.data_nascimento,
        sexo_biologico=usuario.sexo_biologico,
        formulario=usuario.formulario,
        status_formulario=usuario.status_formulario
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario