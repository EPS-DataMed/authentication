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
