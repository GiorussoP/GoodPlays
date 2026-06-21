import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.models import Base
from app.database import get_db
from app.main import app

# Banco SQLite em memória para testes rápidos
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Abre uma conexão explícita que persistirá durante o escopo do teste
    connection = engine.connect()
    
    # Cria as tabelas dentro dessa conexão específica
    Base.metadata.create_all(bind=connection)
    
    # Cria a sessão vinculada diretamente à conexão aberta
    db = TestingSessionLocal(bind=connection)
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=connection)
        connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    # Substitui o banco real pelo banco de testes na aplicação
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_client(client):
    """Gera um usuário de teste, faz login e retorna um cliente autenticado."""
    # 1. Cria o usuário no banco de dados de teste através do client
    client.post(
        "/users/", 
        json={"username": "tester", "email": "tester@teste.com", "password": "123"}
    )
    
    # 2. Faz o login para gerar o Token JWT
    # Nota: Como o seu login usa OAuth2PasswordRequestForm, passamos os dados em 'data' (form), não em 'json'
    response = client.post(
        "/login", 
        data={"username": "tester", "password": "123"}
    )
    token = response.json()["access_token"]
    
    # 3. Injeta o cabeçalho de autorização permanentemente neste cliente
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    # 4. Devolve o cliente pronto e logado para o teste usar
    yield client