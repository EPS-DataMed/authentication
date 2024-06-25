import os
import smtplib
import jwt
import email.message
import base64

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..models import userModel
from ..schemas import emailSchema

load_dotenv()

login = os.getenv("MAIL_USERNAME")
password = os.getenv("MAIL_PASSWORD")

router = APIRouter(
    prefix="/auth",
    tags=["Email"],
)

@router.post("/forgot-password")
async def forgot_password(request: emailSchema.EmailSchema, db: Session = Depends(get_db)):
    existing_user = db.query(userModel.User).filter(userModel.User.email == request.email).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    token_data = {
        "email": request.email,
        "expires": str(datetime.utcnow() + timedelta(hours=24))
    }

    reset_token = jwt.encode(token_data, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    url_safe_token = base64.urlsafe_b64encode(reset_token.encode()).decode().rstrip('=')

    print(url_safe_token)
    html = """
    <!DOCTYPE html>
    <html>
    <title>Recuperação de senha</title>
    <body>
    <div styles="width: 100%; font-family: monospace;">
        <h1>Recuperação de senha</h1>
        <p>Olá, {0}!</p>
        <p>Recebemos uma solicitação de recuperação de senha para sua conta.</p>
        <p>Para redefinir sua senha, clique no link abaixo:</p>
        <a href="{1}/auth/password/{2}/{3}/">Recuperar senha</a>
        <p>Para a sua segurança o link expira em 30 minutos.</p>
        <p>Se você não solicitou a recuperação de senha, ignore este e-mail.</p>
    <div>
    </body>
    </html>
    """.format(existing_user.full_name, os.getenv("FRONTEND_URL"), existing_user.id, url_safe_token)

    message = email.message.Message()
    message["Subject"] = "Recuperação de senha"
    message["From"] = login
    message["To"] = request.email
    message.add_header("Content-Type", "text/html")
    message.set_payload(html)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(login, password)
    server.sendmail(login, request.email, message.as_string().encode("utf-8"))
    print("E-mail enviado com sucesso!") 

    return {"code": 200, "message": "Enviamos um e-mail com as instruções para redefinir sua senha."}
