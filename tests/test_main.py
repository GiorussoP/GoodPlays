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
    
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao GoodPlays API!"}