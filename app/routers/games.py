from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Game
from app.schemas import GameCreate, GameResponse

router = APIRouter(prefix="/games", tags=["Games"])

@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    # Verifica se o jogo já existe pelo título
    db_game = db.query(Game).filter(Game.title == game.title).first()
    if db_game:
        raise HTTPException(status_code=400, detail="Jogo já cadastrado no sistema")
    
    # Cria a instância do modelo
    new_game = Game(
        title=game.title,
        description=game.description,
        developer=game.developer,
        genre=game.genre,
        release_year=game.release_year
    )
    
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    
    return new_game

@router.get("/", response_model=list[GameResponse])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os jogos disponíveis. 
    Usa skip e limit para paginação básica.
    """
    games = db.query(Game).offset(skip).limit(limit).all()
    return games

@router.get("/{game_id}", response_model=GameResponse)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return db_game