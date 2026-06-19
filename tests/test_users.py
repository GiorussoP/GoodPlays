import pytest

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