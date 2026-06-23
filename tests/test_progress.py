import pytest

def test_create_progress_success(auth_client):
    # O auth_client já é um usuário logado ("tester"). Criamos apenas o jogo.
    game_response = auth_client.post("/games/", json={"title": "Progress Game", "developer": "Dev"})
    game_id = game_response.json()["id"]
    
    # O user_id não precisa mais ser enviado, o backend pega do token
    progress_data = {
        "game_id": game_id,
        "progress_percentage": 50,
        "last_played_at": "2023-01-01T10:00:00"
    }
    
    response = auth_client.post("/progress/", json=progress_data)
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert data["data"]["game_id"] == game_id
    assert data["data"]["progress_percentage"] == 50
    assert "user_id" in data["data"] # O backend preencheu automaticamente

def test_create_progress_duplicate(auth_client):
    game_response = auth_client.post("/games/", json={"title": "Progress Game Dup", "developer": "Dev"})
    game_id = game_response.json()["id"]
    
    # Criar progresso pela primeira vez
    auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 50})
    
    # Tentar criar o mesmo progresso novamente
    response = auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 75})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Progress already exists for this user and game."

def test_create_progress_without_login(client):
    # client não tem token de autenticação
    progress_data = {
        "game_id": 1,
        "progress_percentage": 50
    }
    response = client.post("/progress/", json=progress_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."
    

def test_get_progress_success(auth_client):
    game_response = auth_client.post("/games/", json={"title": "Progress Game 2", "developer": "Dev 2"})
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 75})
    
    # Pegamos o user_id que foi injetado pelo backend
    user_id = progress_response.json()["data"]["user_id"]
    
    response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["game_id"] == game_id
    assert data["progress_percentage"] == 75

def test_get_progress_not_found(auth_client):
    response = auth_client.get("/progress/by-user-and-game/999/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Progress not found."

def test_get_progress_without_login(client):
    response = client.get("/progress/by-user-and-game/999/999")
    assert response.status_code == 401

def test_get_user_progress_success(auth_client):
    game1_response = auth_client.post("/games/", json={"title": "Game 1", "developer": "Dev 1"})
    game2_response = auth_client.post("/games/", json={"title": "Game 2", "developer": "Dev 2"})
    
    game1_id = game1_response.json()["id"]
    game2_id = game2_response.json()["id"]
    
    p1 = auth_client.post("/progress/", json={"game_id": game1_id, "progress_percentage": 50})
    auth_client.post("/progress/", json={"game_id": game2_id, "progress_percentage": 75})
    
    user_id = p1.json()["data"]["user_id"]
    
    response = auth_client.get(f"/progress/by-user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["user_id"] == user_id
    assert data[1]["user_id"] == user_id

def test_get_user_progress_not_found(auth_client):
    response = auth_client.get("/progress/by-user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No progress found for this user."

def test_get_user_progress_without_login(client):
    response = client.get("/progress/by-user/999")
    assert response.status_code == 401

def test_get_game_progress_success(auth_client):
    game_response = auth_client.post("/games/", json={"title": "Shared Game", "developer": "Dev"})
    game_id = game_response.json()["id"]
    
    # 1. Cria progresso do primeiro usuário (auth_client já logado)
    auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 30})
    
    # 2. Cria um segundo usuário no banco para testar progressos múltiplos
    auth_client.post("/users/", json={"username": "user2", "email": "user2@test.com", "password": "123"})
    login_res = auth_client.post("/login", data={"username": "user2", "password": "123"})
    token2 = login_res.json()["access_token"]
    
    # 3. Cria progresso forçando o cabeçalho do segundo usuário nesta requisição
    auth_client.post(
        "/progress/", 
        json={"game_id": game_id, "progress_percentage": 60},
        headers={"Authorization": f"Bearer {token2}"}
    )
    
    # 4. Obtém todos os progressos do jogo
    response = auth_client.get(f"/progress/by-game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["game_id"] == game_id
    assert data[1]["game_id"] == game_id

def test_get_game_progress_not_found(auth_client):
    response = auth_client.get("/progress/by-game/999")
    assert response.status_code == 404

def test_get_game_progress_without_login(client):
    response = client.get("/progress/by-game/999")
    assert response.status_code == 401

def test_update_progress_success(auth_client):
    game_response = auth_client.post("/games/", json={"title": "Progress Game 3", "developer": "Dev 3"})
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 30})
    
    user_id = progress_response.json()["data"]["user_id"]
    get_response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    progress_id = get_response.json()["id"]
    
    update_data = {
        "progress_percentage": 60,
        "last_played_at": "2023-01-02T15:00:00"
    }
    
    response = auth_client.put(f"/progress/{progress_id}", json=update_data)
    assert response.status_code == 200
    assert "message" in response.json()

def test_update_progress_not_found(auth_client):
    update_data = {"progress_percentage": 80}
    response = auth_client.put("/progress/999", json=update_data)
    assert response.status_code == 404

def test_update_progress_without_login(client):
    update_data = {"progress_percentage": 80}
    response = client.put("/progress/999", json=update_data)
    assert response.status_code == 401

def test_delete_progress_success(auth_client):
    game_response = auth_client.post("/games/", json={"title": "Progress Game 4", "developer": "Dev 4"})
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={"game_id": game_id, "progress_percentage": 90})
    
    user_id = progress_response.json()["data"]["user_id"]
    get_response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    progress_id = get_response.json()["id"]
    
    response = auth_client.delete(f"/progress/{progress_id}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_progress_not_found(auth_client):
    response = auth_client.delete("/progress/999")
    assert response.status_code == 404

def test_delete_progress_without_login(client):
    response = client.delete("/progress/999")
    assert response.status_code == 401

def test_get_my_progress(auth_client):
    # 1. Arrange: Cria um progresso para o usuário logado
    # (Assumindo que você tenha um game cadastrado)
    game_response = auth_client.post("/games/", json={"title": "God of War"})
    game_id = game_response.json()["id"]
    
    auth_client.post("/progress/", json={
        "game_id": game_id,
        "progress_percentage": 10,
        "last_played_at": "2023-10-10"
    })
    
    # 2. Act: Chama o endpoint de progressão do usuário
    response = auth_client.get("/progress/me")
    
    # 3. Assert
    assert response.status_code == 200
    assert len(response.json()) > 0