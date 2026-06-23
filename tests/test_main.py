from fastapi.testclient import TestClient
from app.main import app

# Inicializa o TestClient com a aplicação principal
client = TestClient(app)

def test_read_root_integration():
    """
    Garante que a aplicação FastAPI sobe corretamente, 
    o roteador está configurado e a rota raiz responde.
    """
    response = client.get("/")
    
    # Verifica se o status code é 200 (OK)
    assert response.status_code == 200
    
    # Verifica se o conteúdo retornado contém partes esperadas do HTML atualizado
    assert "<title>GoodPlays</title>" in response.text
    assert "Bem-vindo ao GoodPlays" in response.text

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_games_page_loads(client):
    response = client.get("/games")
    assert response.status_code == 200

def test_my_progress_page(client):
    response = client.get("/my-progress")
    assert response.status_code == 200