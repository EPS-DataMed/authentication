from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

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