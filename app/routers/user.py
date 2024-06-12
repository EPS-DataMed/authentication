from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import userModel
from ..schemas import userSchema
from ..utils import hash_password

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)

@router.post("/", response_model=userSchema.Usuario)
def create_usuario(usuario: userSchema.UsuarioCreate, db: Session = Depends(get_db)):
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