import pytest
from unittest.mock import patch, MagicMock
from app.database import get_db

@patch("app.database.SessionLocal")
def test_get_db_lifecycle(mock_session_local):
    """
    Testa o ciclo de vida da dependência get_db do database.py.
    Garante que a sessão do banco é gerada e obrigatoriamente fechada.
    """

    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    
    db_generator = get_db()
    db_yielded = next(db_generator)
    
    assert db_yielded == mock_session
    mock_session.close.assert_not_called()
    
    with pytest.raises(StopIteration):
        next(db_generator)
        
    mock_session.close.assert_called_once() # Garante que db.close() foi executado