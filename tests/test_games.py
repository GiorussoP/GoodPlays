import pytest

# --- Testes de Criação (POST) ---

def test_create_game_success(client):
    """Garante que é possível registar um novo jogo com sucesso."""
    payload = {
        "title": "The Legend of Zelda: Breath of the Wild",
        "description": "Uma aventura épica em mundo aberto.",
        "developer": "Nintendo",
        "genre": "Ação/Aventura",
        "release_year": 2017
    }
    response = client.post("/games/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Legend of Zelda: Breath of the Wild"
    assert data["developer"] == "Nintendo"
    assert "id" in data  # Garante que o banco atribuiu um ID

def test_create_game_duplicate_title(client):
    """Garante que o sistema bloqueia a criação de jogos com o mesmo título."""
    # 1. Cria o jogo pela primeira vez
    client.post(
        "/games/", 
        json={"title": "Hollow Knight", "developer": "Team Cherry"}
    )
    
    # 2. Tenta criar exatamente o mesmo jogo
    response = client.post(
        "/games/", 
        json={"title": "Hollow Knight", "developer": "Outro Estúdio"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Jogo já cadastrado no sistema"

# --- Testes de Leitura (GET) ---

def test_read_games_list(client):
    """Garante que a listagem de jogos devolve todos os registos corretamente."""
    # 1. Arrange: Insere dois jogos no banco de dados limpo
    client.post("/games/", json={"title": "Dark Souls", "release_year": 2011})
    client.post("/games/", json={"title": "Bloodborne", "release_year": 2015})
    
    # 2. Act: Pede a lista de jogos
    response = client.get("/games/")
    
    # 3. Assert: Valida a lista devolvida
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Dark Souls"
    assert data[1]["title"] == "Bloodborne"

def test_read_game_by_id_success(client):
    """Garante que é possível encontrar um jogo específico através do seu ID."""
    # 1. Arrange: Cria o jogo e guarda o ID gerado
    create_response = client.post("/games/", json={"title": "Celeste", "genre": "Plataforma"})
    game_id = create_response.json()["id"]
    
    # 2. Act: Procura por esse ID
    response = client.get(f"/games/{game_id}")
    
    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == game_id
    assert data["title"] == "Celeste"

def test_read_game_not_found(client):
    """Garante que o sistema devolve o erro correto 404 se o jogo não existir."""
    response = client.get("/games/9999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Jogo não encontrado"