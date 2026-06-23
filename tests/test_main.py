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
    
    # Verifica se o conteúdo retornado contém partes esperadas do HTML
    assert "<title>GoodPlays</title>" in response.text
    assert "Descubra e Compartilhe os Melhores Jogos" in response.text