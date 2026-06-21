import pytest

def test_create_progress_success(auth_client):
    # Criar usuário e jogo primeiro
    user_response = auth_client.post("/users/", json={"username": "progressuser", "email": "progress@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Progress Game", "developer": "Dev"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    # Criar progresso
    progress_data = {
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 50,
        "last_played_at": "2023-01-01T10:00:00"
    }
    
    response = auth_client.post("/progress/", json=progress_data)
    assert response.status_code == 200
    data = response.json()
    # Ajustar para verificar os campos corretos na resposta
    assert "message" in data
    assert data["data"]["user_id"] == user_id
    assert data["data"]["game_id"] == game_id
    assert data["data"]["progress_percentage"] == 50

def test_create_progress_duplicate(auth_client):
    # Criar usuário e jogo primeiro
    user_response = auth_client.post("/users/", json={"username": "progressuser_dup", "email": "progress_dup@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Progress Game Dup", "developer": "Dev"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    # Criar progresso pela primeira vez
    auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 50
    })
    
    # Tentar criar o mesmo progresso novamente
    response = auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 75
    })
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Progress already exists for this user and game."

def test_get_progress_success(auth_client):
    # Criar usuário, jogo e progresso
    user_response = auth_client.post("/users/", json={"username": "progressuser2", "email": "progress2@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Progress Game 2", "developer": "Dev 2"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 75
    })
    
    # Obter progresso usando a rota correta: /progress/by-user-and-game/{user_id}/{game_id}
    response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["game_id"] == game_id
    assert data["progress_percentage"] == 75

def test_get_progress_not_found(auth_client):
    # Tentar obter progresso que não existe
    response = auth_client.get("/progress/by-user-and-game/999/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Progress not found."

def test_get_user_progress_success(auth_client):
    # Criar usuário e jogos
    user_response = auth_client.post("/users/", json={"username": "userprogress", "email": "userprogress@test.com", "password": "pass123"})
    game1_response = auth_client.post("/games/", json={"title": "Game 1", "developer": "Dev 1"})
    game2_response = auth_client.post("/games/", json={"title": "Game 2", "developer": "Dev 2"})
    
    user_id = user_response.json()["id"]
    game1_id = game1_response.json()["id"]
    game2_id = game2_response.json()["id"]
    
    # Criar progressos para o usuário em diferentes jogos
    auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game1_id,
        "progress_percentage": 50
    })
    
    auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game2_id,
        "progress_percentage": 75
    })
    
    # Obter todos os progressos do usuário
    response = auth_client.get(f"/progress/by-user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["user_id"] == user_id
    assert data[1]["user_id"] == user_id

def test_get_user_progress_not_found(auth_client):
    # Tentar obter progressos de um usuário que não tem progressos
    response = auth_client.get("/progress/by-user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No progress found for this user."

def test_get_game_progress_success(auth_client):
    # Criar usuários e jogo
    user1_response = auth_client.post("/users/", json={"username": "user1progress", "email": "user1progress@test.com", "password": "pass123"})
    user2_response = auth_client.post("/users/", json={"username": "user2progress", "email": "user2progress@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Shared Game", "developer": "Dev"})
    
    user1_id = user1_response.json()["id"]
    user2_id = user2_response.json()["id"]
    game_id = game_response.json()["id"]
    
    # Criar progressos de diferentes usuários no mesmo jogo
    auth_client.post("/progress/", json={
        "user_id": user1_id,
        "game_id": game_id,
        "progress_percentage": 30
    })
    
    auth_client.post("/progress/", json={
        "user_id": user2_id,
        "game_id": game_id,
        "progress_percentage": 60
    })
    
    # Obter todos os progressos do jogo
    response = auth_client.get(f"/progress/by-game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["game_id"] == game_id
    assert data[1]["game_id"] == game_id

def test_get_game_progress_not_found(auth_client):
    # Tentar obter progressos de um jogo que não tem progressos
    response = auth_client.get("/progress/by-game/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No progress found for this game."

def test_update_progress_success(auth_client):
    # Criar usuário, jogo e progresso
    user_response = auth_client.post("/users/", json={"username": "progressuser3", "email": "progress3@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Progress Game 3", "developer": "Dev 3"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 30
    })
    
    # Primeiro, precisamos obter o ID do progresso criado
    get_response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    progress_id = get_response.json()["id"]
    
    # Atualizar progresso
    update_data = {
        "progress_percentage": 60,
        "last_played_at": "2023-01-02T15:00:00"
    }
    
    response = auth_client.put(f"/progress/{progress_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_update_progress_not_found(auth_client):
    # Tentar atualizar um progresso que não existe
    update_data = {
        "progress_percentage": 80
    }
    
    response = auth_client.put("/progress/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Progress entry not found."

def test_delete_progress_success(auth_client):
    # Criar usuário, jogo e progresso
    user_response = auth_client.post("/users/", json={"username": "progressuser4", "email": "progress4@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Progress Game 4", "developer": "Dev 4"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    progress_response = auth_client.post("/progress/", json={
        "user_id": user_id,
        "game_id": game_id,
        "progress_percentage": 90
    })
    
    # Primeiro, precisamos obter o ID do progresso criado
    get_response = auth_client.get(f"/progress/by-user-and-game/{user_id}/{game_id}")
    progress_id = get_response.json()["id"]
    
    # Deletar progresso
    response = auth_client.delete(f"/progress/{progress_id}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_progress_not_found(auth_client):
    # Tentar deletar um progresso que não existe
    response = auth_client.delete("/progress/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Progress entry not found."