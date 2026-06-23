def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert "Register" in response.text


def test_games_page(client):
    response = client.get("/games")
    assert response.status_code == 200
    assert "Browse Games" in response.text
def test_game_detail_page(client):
    # Primeiro, criar um jogo para testar a página de detalhes
    from app.models import Game
    from app.database import SessionLocal
    import time

    db = SessionLocal()
    # Usar um título único para evitar conflitos com UNIQUE constraint
    unique_title = f"Test Game {int(time.time() * 1000000)}"
    game = Game(
        title=unique_title,
        description="A test game",
        developer="Test Dev",
        genre="Test Genre",
        release_year=2023,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    game_id = game.id
    db.close()

    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    # Verificar elementos que estão presentes no HTML bruto
    assert "gameDetailContent" in response.text
    assert str(game_id) in response.text

def test_profile_page(auth_client):
    response = auth_client.get("/profile")
    assert response.status_code == 200
    assert "Profile" in response.text