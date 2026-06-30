import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User, Review, Game

client = TestClient(app)

def test_create_review_success(auth_client):
    # Primeiro criar usuário e jogo
    user_response = auth_client.post("/users/", json={"username": "testuser", "email": "test@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game", "developer": "Test Dev"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    # Criar review
    review_data = {
        "user_id": user_id,
        "game_id": game_id,
        "rating": 5,
        "comment": "Excelente jogo!"
    }
    
    response = auth_client.post("/reviews/", json=review_data)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Excelente jogo!"
    assert "id" in data

def test_create_review_without_login(client):
    review_data = {
        "user_id": 1,
        "game_id": 1,
        "rating": 5,
        "comment": "Excelente jogo!"
    }
    
    response = client.post("/reviews/", json=review_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."

def test_create_review_invalid_rating(auth_client):
    review_data = {
        "user_id": 1,
        "game_id": 1,
        "rating": 10,  # Inválido
        "comment": "Muito bom"
    }
    
    response = auth_client.post("/reviews/", json=review_data)
    assert response.status_code == 422

def test_get_review_success(auth_client):
    # Criar usuário, jogo e review
    user_response = auth_client.post("/users/", json={"username": "testuser2", "email": "test2@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game 2", "developer": "Test Dev 2"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    review_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 4,
        "comment": "Bom jogo"
    })
    
    review_id = review_response.json()["id"]
    
    # Obter review
    response = auth_client.get(f"/reviews/{review_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == review_id
    assert data["rating"] == 4

def test_get_review_not_found(auth_client):
    response = auth_client.get("/reviews/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_get_review_without_login(client):
    
    response = client.get("/reviews/9999")
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."

def test_update_review_success(auth_client):
    # Criar usuário, jogo e review
    user_response = auth_client.post("/users/", json={"username": "testuser3", "email": "test3@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game 3", "developer": "Test Dev 3"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    review_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 3,
        "comment": "Jogo médio"
    })
    
    review_id = review_response.json()["id"]
    
    # Atualizar review
    update_data = {"rating": 5, "comment": "Jogo excelente!"}
    response = auth_client.put(f"/reviews/{review_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Jogo excelente!"

def test_delete_review_success(auth_client):
    # Criar usuário, jogo e review
    user_response = auth_client.post("/users/", json={"username": "testuser4", "email": "test4@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game 4", "developer": "Test Dev 4"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    review_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 2,
        "comment": "Ruim"
    })
    
    review_id = review_response.json()["id"]
    
    # Deletar review
    response = auth_client.delete(f"/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted successfully"
    
    # Verificar que foi deletado
    get_response = auth_client.get(f"/reviews/{review_id}")
    assert get_response.status_code == 404

def test_get_game_reviews_success(auth_client):
    # Criar usuário, jogo e review
    user_response = auth_client.post("/users/", json={"username": "testuser5", "email": "test5@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game 5", "developer": "Test Dev 5"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    # Criar múltiplas reviews para o jogo
    review1_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 5,
        "comment": "Excelente jogo!"
    })
    
    review2_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 4,
        "comment": "Bom jogo"
    })
    
    # Obter todas as reviews para o jogo
    response = auth_client.get(f"/reviews/game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Verificar os dados das reviews
    for review in data:
        assert review["rating"] in [4, 5]
        assert "comment" in review
        assert "id" in review

def test_get_game_reviews_empty(auth_client):
    response = auth_client.get("/reviews/game/9999")
    assert response.status_code == 200
    assert response.json() == []  # Espera uma lista vazia

def test_get_game_reviews_without_login(client):
    response = client.get("/reviews/game/9999")
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."

def test_update_review_invalid_rating(auth_client):
    # Criar usuário, jogo e review
    user_response = auth_client.post("/users/", json={"username": "testuser6", "email": "test6@test.com", "password": "pass123"})
    game_response = auth_client.post("/games/", json={"title": "Test Game 6", "developer": "Test Dev 6"})
    
    user_id = user_response.json()["id"]
    game_id = game_response.json()["id"]
    
    review_response = auth_client.post("/reviews/", json={
        "user_id": user_id,
        "game_id": game_id,
        "rating": 3,
        "comment": "Jogo médio"
    })
    
    review_id = review_response.json()["id"]
    
    # Tentar atualizar com rating inválido
    update_data = {"rating": 10, "comment": "Muito bom"}
    response = auth_client.put(f"/reviews/{review_id}", json=update_data)
    
    assert response.status_code == 422
    
    # Converte a lista de erros do Pydantic para string para checar o conteúdo
    errors_str = str(response.json()["detail"])
    assert "rating" in errors_str
    assert "must be between 1 and 5" in errors_str

def test_delete_review_not_found(auth_client):
    response = auth_client.delete("/reviews/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_delete_review_without_login(client):
    response = client.delete("/reviews/9999")
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."

def test_update_review_not_found(auth_client):
    # Dados para a tentativa de atualização
    update_data = {
        "rating": 5, 
        "comment": "Tentando atualizar uma review que não existe"
    }
    
    # Faz o PUT para um ID inexistente (9999)
    response = auth_client.put("/reviews/9999", json=update_data)
    
    # Valida se a API respondeu com 404 e a mensagem correta
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_update_review_without_login(client):
    
    update_data = {
        "rating": 5, 
        "comment": "Tentando atualizar uma review que não existe"
    }
    
    response = client.put("/reviews/9999", json=update_data)  
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais. Faça login novamente."



def test_create_review_uses_authenticated_user_id(db_session, auth_client):
    """
    Bug Fix Test: Ensure that the user_id in the created review
    matches the authenticated user, not the one sent in the payload.
    """
    # Create a game to associate the review with
    game = Game(title="Test Game", description="A test game")
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)

# Attempt to create a review with a DIFFERENT user_id in the payload
    response = auth_client.post(
        "/reviews/",
        json={
            "user_id": 999,  # Intentionally wrong user_id
            "game_id": game.id,
            "rating": 5,
            "comment": "Great game!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    
    # Verify that the review was created for the current user, NOT user_id 999
    review_in_db = db_session.query(Review).filter(Review.id == data['id']).first()
    
    # Get the current user's ID
    current_user = db_session.query(User).filter(User.username == "tester").first()
    
    assert review_in_db.user_id == current_user.id
    assert review_in_db.user_id != 999  # Ensure the malicious payload was ignored


def test_delete_review_unauthorized(db_session, auth_client):
    """
    Bug Fix Test: Ensure that a user cannot delete a review belonging to another user.
    """
    # Create a game
    game = Game(title="Test Game 2", description="Another test game")
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)

    # Create a review for user 1
    review1 = Review(user_id=1, game_id=game.id, rating=5, comment="Good")
    db_session.add(review1)
    db_session.commit()
    db_session.refresh(review1)
    
    # Simulate a review belonging to a different user (user 999)
    review1.user_id = 999
    db_session.commit()
    
# Now try to delete it as the current user (user 1)
    response = auth_client.delete(f"/reviews/{review1.id}")
    
    assert response.status_code == 403  # Should be forbidden
    
    # Verify the review is still in the database
    review_in_db = db_session.query(Review).filter(Review.id == review1.id).first()
    assert review_in_db is not None  # Should not have been deleted


def test_update_review_unauthorized(db_session, auth_client):
    """
    Bug Fix Test: Ensure that a user cannot update a review belonging to another user.
    """
    # Create a game
    game = Game(title="Test Game 3", description="Third test game")
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)

    # Create a review for user 1
    review1 = Review(user_id=1, game_id=game.id, rating=5, comment="Good")
    db_session.add(review1)
    db_session.commit()
    db_session.refresh(review1)
    
    # Simulate a review belonging to a different user
    review1.user_id = 999
    db_session.commit()
    
# Try to update it as the current user (user 1)
    response = auth_client.put(
        f"/reviews/{review1.id}",
        json={
            "rating": 3,
            "comment": "Updated comment"
        }
    )
    
    assert response.status_code == 403  # Should be forbidden
    
    # Verify the review was not updated
    review_in_db = db_session.query(Review).filter(Review.id == review1.id).first()
    assert review_in_db.comment == "Good"  # Should remain unchanged