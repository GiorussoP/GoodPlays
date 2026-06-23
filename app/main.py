from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.routers import users, games, auth, progress, reviews
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Game
import os

# Cria as tabelas no banco SQLite automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

# Seed de jogos iniciais para a aplicação
def seed_games():
    db: Session = SessionLocal()
    try:
        if db.query(Game).count() == 0:
            sample_games = [
                Game(title="The Legend of Zelda: Breath of the Wild", description="An open-world adventure game for Nintendo Switch", developer="Nintendo", genre="Adventure", release_year=2017),
                Game(title="Minecraft", description="A sandbox game about placing blocks and going on adventures.", developer="Mojang Studios", genre="Simulation", release_year=2011),
                Game(title="Hades", description="A roguelike dungeon crawler from Supergiant Games.", developer="Supergiant Games", genre="Action", release_year=2020),
                Game(title="Stardew Valley", description="A farming simulation role-playing game.", developer="ConcernedApe", genre="Simulation", release_year=2016),
                Game(title="Celeste", description="A platformer about climbing a mountain and overcoming challenges.", developer="Matt Makes Games", genre="Platformer", release_year=2018)
            ]
            db.add_all(sample_games)
            db.commit()
    finally:
        db.close()

seed_games()

app = FastAPI(title="GoodPlays API")

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Inclui as rotas do módulo de usuários
app.include_router(users.router)
app.include_router(games.router)
app.include_router(auth.router)
app.include_router(progress.router)
app.include_router(reviews.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
        request=request
    )

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        context={"request": request},
        request=request
    )

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        name="register.html",
        context={"request": request},
        request=request
    )

@app.get("/games", response_class=HTMLResponse)
def games_page(request: Request):
    return templates.TemplateResponse(
        name="games.html",
        context={"request": request},
        request=request
    )

@app.get("/game/{game_id}", response_class=HTMLResponse)
def game_detail_page(request: Request, game_id: int):
    return templates.TemplateResponse(
        name="game-detail.html",
        context={"request": request, "game_id": game_id},
        request=request
    )

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse(
        name="profile.html",
        context={"request": request},
        request=request
    )