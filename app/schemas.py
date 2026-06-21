from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    developer: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None

class GameCreate(GameBase):
    pass # Herda tudo de GameBase, sem nada a mais por enquanto

class GameResponse(GameBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProgressCreate(BaseModel):
    user_id: int
    game_id: int
    progress_percentage: int
    last_played_at: Optional[str] = None

class ProgressUpdate(BaseModel):
    progress_percentage: Optional[int] = None
    last_played_at: Optional[str] = None

class ProgressResponse(ProgressCreate):
    id: int
    created_at: Optional[str] = None
