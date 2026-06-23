import jwt
from fastapi import HTTPException
import datetime  # Adicionado
from app.routers.auth import get_current_user, SECRET_KEY, ALGORITHM  # Mantido
from app.models import User
from app.database import SessionLocal, get_db


def test_get_current_user_invalid_token(client):
    # Testar com token inválido
    try:
        get_current_user(token="invalid_token", db=client.app.dependency_overrides.get(SessionLocal, lambda: SessionLocal())())
    except HTTPException as e:
        assert e.status_code == 401
        assert "Não foi possível validar as credenciais" in e.detail


def test_get_current_user_missing_username(client):
    # Criar um token sem o campo "sub"
    token = jwt.encode({"exp": 9999999999}, SECRET_KEY, algorithm=ALGORITHM)
    try:
        get_current_user(token=token, db=client.app.dependency_overrides.get(SessionLocal, lambda: SessionLocal())())
    except HTTPException as e:
        assert e.status_code == 401
        assert "Não foi possível validar as credenciais" in e.detail


def test_get_current_user_user_not_found(client):
    # Criar um token para um usuário que não existe
    token = jwt.encode({"sub": "nonexistent_user", "exp": 9999999999}, SECRET_KEY, algorithm=ALGORITHM)
    try:
        get_current_user(token=token, db=client.app.dependency_overrides.get(SessionLocal, lambda: SessionLocal())())
    except HTTPException as e:
        assert e.status_code == 401
        assert "Não foi possível validar as credenciais" in e.detail

def test_get_current_user_valid_token(auth_client):
    # O auth_client fixture já criou o usuário "tester" e fez login
    # Vamos gerar um novo token manualmente para testar a função get_current_user
    
    # Gerar token manualmente com timezone-aware datetime
    token = jwt.encode(
        {
            "sub": "tester",
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    # Obter a sessão de teste correta através do client
    # O auth_client usa o client que tem o override do banco de testes
    db = next(auth_client.app.dependency_overrides[get_db]())
    
    try:
        returned_user = get_current_user(token=token, db=db)
        assert returned_user.username == "tester"
    finally:
        db.close()