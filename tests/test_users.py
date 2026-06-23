import pytest
from app.models import User
from app.routers.auth import get_current_user

# --- Testes de Unidade (Comportamentos isolados) ---

def test_create_user_success(client):
    response = client.post(
        "/users/", 
        json={"username": "giovanni", "email": "gio@teste.com", "password": "123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "giovanni"
    assert data["email"] == "gio@teste.com"
    assert "id" in data

def test_create_user_duplicate_email(client):
    # Cria o primeiro usuário
    client.post("/users/", json={"username": "user1", "email": "duplo@teste.com", "password": "123"})
    # Tenta criar o segundo com o mesmo email
    response = client.post("/users/", json={"username": "user2", "email": "duplo@teste.com", "password": "321"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado"

def test_create_user_duplicate_username(client):
    client.post("/users/", json={"username": "mesmonome", "email": "email1@teste.com", "password": "123"})
    response = client.post("/users/", json={"username": "mesmonome", "email": "email2@teste.com", "password": "321"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Username já em uso"

def test_create_user_invalid_email(client):
    response = client.post("/users/", json={"username": "invalido", "email": "emailerrado", "password": "123"})
    assert response.status_code == 422 # Pydantic bloqueia erro de validação (EmailStr)

def test_read_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"

def test_read_user_success(client):
    response = client.post(
        "/users/", 
        json={"username": "victor", "email": "victor@teste.com", "password": "secure123"}
    )
    assert response.status_code == 201
    created_user = response.json()
    user_id = created_user["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "victor"
    assert data["email"] == "victor@teste.com"

def test_read_current_user_success(client): # Removido o 'app' daqui
    # 1. Criamos um usuário fictício que simula o usuário logado
    mock_user = User(id=1, username="test_me", email="me@teste.com")

    # 2. Substituímos a dependência usando client.app
    client.app.dependency_overrides[get_current_user] = lambda: mock_user

    # 3. Fazemos a requisição para a rota /me
    response = client.get("/users/me")

    # 4. Limpamos os overrides no client.app para não afetar outros testes
    client.app.dependency_overrides.clear()

    # 5. Validações
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "test_me"
    assert data["email"] == "me@teste.com"