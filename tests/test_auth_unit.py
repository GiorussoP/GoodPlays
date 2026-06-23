import pytest
import jwt
from fastapi import HTTPException
from app.routers.auth import get_current_user, SECRET_KEY, ALGORITHM
from app.models import User

def test_get_current_user_no_sub_in_payload(db_session):
    """
    Cria um token válido (decodificável), mas sem o campo 'sub'.
    Isso deve cair no 'if username is None'.
    """
    token = jwt.encode({"exp": 9999999999}, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc:
        get_current_user(token=token, db=db_session)
    
    assert exc.value.status_code == 401

# --- Teste para: if user is None (usuário não existe no banco) ---
def test_get_current_user_user_not_found_in_db(db_session):
    """
    Cria um token para um usuário 'inexistente', 
    para forçar o db.query a retornar None.
    """
    token = jwt.encode({"sub": "usuario_fantasma", "exp": 9999999999}, SECRET_KEY, algorithm=ALGORITHM)
    
    # db_session está vazio, então 'usuario_fantasma' não será encontrado
    with pytest.raises(HTTPException) as exc:
        get_current_user(token=token, db=db_session)
    
    assert exc.value.status_code == 401