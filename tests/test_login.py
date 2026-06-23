def test_login_success(client):
    """Garante que um usuário com credenciais corretas recebe um Token JWT."""
    # 1. Prepara o terreno: Cria um usuário válido no banco de testes
    client.post(
        "/users/", 
        json={"username": "mario", "email": "mario@cogumelo.com", "password": "super_senha"}
    )
    
    # 2. Ação: Tenta fazer o login
    # Lembrete: A rota de login usa OAuth2PasswordRequestForm, então enviamos 'data' e não 'json'
    response = client.post(
        "/login",
        data={"username": "mario", "password": "super_senha"}
    )
    
    # 3. Validação: Checa se deu 200 OK e se o token veio no formato correto
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    # Garante que o token é uma string real e não está vazio
    assert len(data["access_token"]) > 0 


def test_login_wrong_password(client):
    """Garante que o sistema bloqueia o acesso se a senha estiver errada."""
    # 1. Prepara o terreno: Cria o usuário
    client.post(
        "/users/", 
        json={"username": "luigi", "email": "luigi@cogumelo.com", "password": "senha_correta"}
    )
    
    # 2. Ação: Tenta fazer o login com a senha errada
    response = client.post(
        "/login",
        data={"username": "luigi", "password": "senha_errada_123"}
    )
    
    # 3. Validação: Checa se foi barrado com 401 e a mensagem correta
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"


def test_login_nonexistent_user(client):
    """Garante que o sistema bloqueia tentativas de login de usuários fantasmas."""
    # 1. Ação direta: Tenta logar sem ter criado o usuário antes
    response = client.post(
        "/login",
        data={"username": "bowser_fantasma", "password": "123"}
    )
    
    # 2. Validação: Checa se foi barrado de forma idêntica (boa prática de segurança)
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"


def test_get_current_user_no_token(client):
    # Tenta acessar um endpoint protegido sem token
    response = client.post("/games/", json={"title": "Sem Token"})
    assert response.status_code == 401
    assert "Não foi possível validar" in response.json()["detail"]

def test_get_current_user_invalid_token(client):
    # Tenta acessar com um token malformado/inválido
    response = client.post(
        "/games/", 
        json={"title": "Token Invalido"},
        headers={"Authorization": "Bearer token_falso_123"}
    )
    assert response.status_code == 401

def test_get_current_user_no_token(client):
    # Tenta acessar um endpoint protegido sem cabeçalho Authorization
    # (A rota /progress/me exige autenticação)
    response = client.get("/progress/me")
    
    assert response.status_code == 401
    assert "Não foi possível validar as credenciais" in response.json()["detail"]

def test_get_current_user_invalid_token(client):
    # Tenta acessar com um token malformado
    response = client.get(
        "/progress/me", 
        headers={"Authorization": "Bearer token_invalido_de_teste"}
    )

    assert response.status_code == 401
    assert "Não foi possível validar as credenciais" in response.json()["detail"]

def test_get_current_user_no_token(client):
    """
    Testa o caso onde não existe header de autorização (token is None).
    Usamos um endpoint protegido (ex: POST /games/) sem passar o token.
    """
    response = client.post("/games/", json={
        "title": "Teste sem Token", 
        "description": "Desc", 
        "developer": "Dev"
    })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."

def test_get_current_user_invalid_token(client):
    """
    Testa o caso onde o token é enviado, mas é inválido/corrompido.
    O jwt.decode falhará, caindo no except jwt.InvalidTokenError.
    """
    response = client.post(
        "/games/", 
        json={"title": "Teste Token Invalido", "description": "Desc", "developer": "Dev"},
        headers={"Authorization": "Bearer token-malformado-aqui"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."