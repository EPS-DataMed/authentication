import base64
import jwt
from datetime import datetime
import requests
import os
from fastapi import HTTPException

def verify_password(plain_password: str, decrypted_password: str) -> bool:
    return plain_password == decrypted_password

def decrypt_password(encrypted_password: str) -> str:
    url = os.getenv("URL_DECRYPT")
    private_key = os.getenv("PRIVATE_KEY")
    data = {
        "message": encrypted_password,
        "private_key": private_key,
    }
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error decrypting password")
    
    return response.json()["decrypted_message"]

def encrypt_password(password: str) -> str:
    url = os.getenv("URL_CYPHER")
    public_key = os.getenv("PUBLIC_KEY")
    data = {
        "message": password,
        "public_key": public_key,
    }
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error encrypting password")
    
    return response.json()["encrypted_message"]

def decode_and_validate_token(token: str):
    try:
        padding = '=' * (4 - (len(token) % 4))
        url_safe_token = token + padding
        
        jwt_token = base64.urlsafe_b64decode(url_safe_token.encode()).decode()
        
        token_data = jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        
        expires = datetime.strptime(token_data["expires"], '%Y-%m-%d %H:%M:%S.%f')
        if datetime.utcnow() > expires:
            return False
        
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
        return False