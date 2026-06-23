from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.routers.auth import get_password_hash, get_current_user
from fastapi import Depends

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username já em uso")

    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/me', response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user