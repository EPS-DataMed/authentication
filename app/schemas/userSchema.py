from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioOut(BaseModel):
    id: int
    nome_completo: str
    email: EmailStr
    data_nascimento: date
    sexo_biologico: str
    data_criacao: datetime
    status_formulario: str
    formulario: Optional[dict] = None

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    user_id: int = None

class UsuarioBase(BaseModel):
    nome_completo: str = Field(..., max_length=255)
    email: EmailStr
    data_nascimento: date
    sexo_biologico: str = Field(..., max_length=1, pattern='^(M|F)$')
    formulario: Optional[dict] = None
    status_formulario: Optional[str] = Field('Não iniciado', pattern='^(Preenchido|Em andamento|Não iniciado)$')

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)

class UsuarioUpdate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    data_criacao: datetime
    senha: str

    class Config:
        orm_mode = True