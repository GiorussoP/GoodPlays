from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

# Configurações do JWT (Em produção, guarde a SECRET_KEY em um arquivo .env)
SECRET_KEY = "uma_chave_super_secreta_muito_longa_de_32_chars!!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["Authentication"])

# --- FUNÇÕES DE SEGURANÇA ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano bate com o hash do banco"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Gera o hash seguro da senha"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Cria o token JWT"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- ROTA DE LOGIN ---

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. O OAuth2PasswordRequestForm espera nativamente os campos 'username' e 'password'
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 2. Checa se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Gera o token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # O FastAPI exige que o retorno tenha exatamente este formato
    return {"access_token": access_token, "token_type": "bearer"}

# O FastAPI precisa saber qual é a URL que gera o token para avisar o Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Esta é a fechadura. Ela recebe o token, decodifica e devolve o usuário logado."""
    
    # O erro padrão caso o token seja inválido, falso ou expirado
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception
    
    try:
        # Tenta abrir o token usando a sua chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        # Se o token estiver vencido ou adulterado, cai aqui e barra o usuário
        raise credentials_exception
        
    # Busca o usuário no banco para garantir que ele ainda existe (não foi deletado)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user