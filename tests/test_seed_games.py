from app.main import seed_games
from app.models import Game
from app.database import SessionLocal


def test_seed_games():
    # Limpar banco antes do teste
    db = SessionLocal()
    db.query(Game).delete()
    db.commit()

    # Chamar seed_games
    seed_games()

    # Verificar se jogos foram criados
    games = db.query(Game).all()
    assert len(games) > 0
    assert games[0].title == "The Legend of Zelda: Breath of the Wild"

    db.close()