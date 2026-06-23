from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.routers import users, games, auth, progress, reviews
import os

# Cria as tabelas no banco SQLite automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GoodPlays API")

# Configuração de arquivos estáticos e templates
#app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
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
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"request": request}
    )

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="register.html", 
        context={"request": request}
    )

@app.get("/games", response_class=HTMLResponse)
def games_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="games.html", 
        context={"request": request}
    )

@app.get("/my-progress", response_class=HTMLResponse)
def my_progress_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="my_progress.html", 
        context={"request": request}
    )