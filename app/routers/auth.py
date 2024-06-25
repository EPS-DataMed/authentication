from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..utils import decode_and_validate_token

from ..models import userModel
from .. import database, oauth2, utils

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(userModel.User).filter(userModel.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    decrypted_password = utils.decrypt_password(user.password)

    if not utils.verify_password(user_credentials.password, decrypted_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/validation-email-token")
def validate_token(token: str):
    is_valid = decode_and_validate_token(token)
    return {"is_valid": is_valid}
