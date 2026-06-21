from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, games, auth, progress

# Cria as tabelas no banco SQLite automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GoodPlays API")

# Inclui as rotas do módulo de usuários
app.include_router(users.router)
app.include_router(games.router)
app.include_router(auth.router)
app.include_router(progress.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao GoodPlays API!"}