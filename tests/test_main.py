from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import userModel
from app.utils import encrypt_password
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Função para obter a sessão de banco de dados para os testes
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuração do cliente de teste
@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.rollback()
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the authentication API"}

# Função de criação de usuário para testes
def create_test_user(db):
    password = "test_password"
    hashed_password = encrypt_password(password)
    birth_date = datetime.strptime("2000-01-01", "%Y-%m-%d").date()
    user = userModel.User(
        id=2,
        full_name="Test User",
        email="testes@example.com",
        password=hashed_password,
        birth_date=birth_date,
        biological_sex="M"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Teste para criação de usuário
def test_create_user(client, db):
    new_user = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "test_password",
        "birth_date": "2000-01-01",
        "biological_sex": "M"
    }
    response = client.post("/auth/users", json=new_user)
    assert response.status_code == 200
    assert response.json()["email"] == new_user["email"]

# Teste para criação de usuário já existente
def test_create_user_fail(client, db):
    new_user = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "test_password",
        "birth_date": "2000-01-01",
        "biological_sex": "M"
    }
    response = client.post("/auth/users", json=new_user)
    assert response.status_code == 400

# Teste para comparação de senha
def test_compare_password(client, db):
    user = create_test_user(db)
    password_data = {
        "password": "test_password"
    }
    response = client.post(f"/auth/users/{user.id}/compare-password", json=password_data)
    assert response.status_code == 200
    assert response.json() is True
    db.delete(user)
    db.commit()

# Teste para comparação de senha de usuário inexistente
def test_compare_password_fail(client, db):
    password_data = {
        "password": "test_password"
    }
    response = client.post(f"/auth/users/999/compare-password", json=password_data)
    assert response.status_code == 404

# Teste para atualização de senha
def test_update_password(client, db):
    user = create_test_user(db)
    new_password = {
        "password": "new_test_password"
    }
    response = client.put(f"/auth/users/{user.id}/password", json=new_password)
    assert response.status_code == 200
    assert response.json()["id"] == user.id
    db.delete(user)
    db.commit()

# Teste para atualização de senha de usuário inexistente
def test_update_password_fail(client):
    new_password = {
        "password": "new_test_password"
    }
    response = client.put(f"/auth/users/999/password", json=new_password)
    assert response.status_code == 404

# Teste para recuperação de senha
def test_forgot_password(client, db):
    user = create_test_user(db)
    email_data = {
        "email": user.email
    }
    response = client.post("/auth/forgot-password", json=email_data)
    assert response.status_code == 200
    assert "Enviamos um e-mail com as instruções para redefinir sua senha." in response.json()["message"]
    db.delete(user)
    db.commit()

# Teste para recuperação de senha de usuário inexistente
def test_forgot_password_fail(client, db):
    email_data = {
        "email": "user@email.com"
    }
    response = client.post("/auth/forgot-password", json=email_data)
    assert response.status_code == 400

# Teste para criação de médico
def test_create_doctor(client, db):
    new_user = create_test_user(db)
    new_doctor = {
        "user_id": 1,
        "crm": "12345",
        "specialty": "Cardiologia"
    }
    response = client.post("/auth/doctors", json=new_doctor)
    assert response.status_code == 200
    db.delete(new_user)
    db.commit()

# Teste para criação de médico com usuário inexistente
def test_create_doctor_fail(client, db):
    new_doctor = {
        "user_id": 999,
        "crm": "12345",
        "specialty": "Cardiologia"
    }
    response = client.post("/auth/doctors", json=new_doctor)
    assert response.status_code == 400

# Teste para criação de médico já inexistente
def test_create_doctor_fail2(client, db):
    new_doctor = {
        "user_id": 1,
        "crm": "12345",
        "specialty": "Cardiologia"
    }
    response = client.post("/auth/doctors", json=new_doctor)
    assert response.status_code == 400

# Teste de rota de autenticação: /auth/login
def test_login(client):
    response = client.post("/auth/login", data={"username": "test@example.com", "password": "test_password"})
    assert response.status_code == 200

# Teste de rota de autenticação: /auth/login para usuário inexistente
def test_login_fail(client):
    response = client.post("/auth/login", data={"username": "testefail@example.com", "password": "test_password"})
    assert response.status_code == 403

# Teste de rota de autenticação: /auth/login para senha incorreta
def test_login_fail2(client):
    response = client.post("/auth/login", data={"username": "test@example.com", "password": "test_password_fail"})
    assert response.status_code == 403