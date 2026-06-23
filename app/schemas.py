from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
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

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    progress_percentage: int
    last_played_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    user_id: int
    game_id: int
    rating: int  # 1-5 scale
    
    @field_validator('rating')
    @classmethod
    def rating_must_be_between_1_and_5(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    comment: Optional[str] = None

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

    @field_validator('rating')
    @classmethod
    def rating_must_be_between_1_and_5(cls, v):
        # Como é opcional, só valida se o valor for enviado
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class UserInReview(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(ReviewCreate):
    id: int
    created_at: Optional[str] = None
    user: Optional[UserInReview] = None

    model_config = ConfigDict(from_attributes=True)