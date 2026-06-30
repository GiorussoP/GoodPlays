from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, database
from app.models import Progress, Review, User, Game
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])  

@router.post("/")
async def create_progress(
    progress: schemas.ProgressCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new progress entry for a user and game."""
    existing_progress = db.query(Progress).filter(
        Progress.user_id == progress.user_id,
        Progress.game_id == progress.game_id
    ).first()
    
    if existing_progress:
        raise HTTPException(
            status_code=400, 
            detail="Progress already exists for this user and game."  
        )
    
    db_progress = Progress(
        user_id=progress.user_id,
        game_id=progress.game_id,
        progress_percentage=progress.progress_percentage,
        last_played_at=progress.last_played_at
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    
    return {
        "message": "Progress created successfully.",
        "data": progress.model_dump()  # Corrigido de .dict() para .model_dump()
    }

@router.get("/by-user-and-game/{user_id}/{game_id}", response_model=schemas.ProgressResponse)
async def get_progress(
    user_id: int, 
    game_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for a specific user and game."""
    progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.game_id == game_id
    ).first()
    
    if not progress:
        raise HTTPException(
            status_code=404, 
            detail="Progress not found."  
        )
    
    return progress

@router.get("/by-user/{user_id}", response_model=List[schemas.ProgressResponse])
async def get_user_progress(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all progress entries for a specific user."""
    progress_entries = db.query(Progress).filter(Progress.user_id == user_id).all()
    
    if not progress_entries:
        raise HTTPException(
            status_code=404, 
            detail="No progress found for this user."  
        )
    
    # Enhance each progress entry with game details
    result = []
    for entry in progress_entries:
        game = db.query(Game).filter(Game.id == entry.game_id).first()
        progress_dict = entry.__dict__.copy()
        progress_dict["game"] = game
        result.append(progress_dict)
    
    return result

@router.get("/by-game/{game_id}", response_model=List[schemas.ProgressResponse])
async def get_game_progress(
    game_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all progress entries for a specific game."""
    progress = db.query(Progress).filter(Progress.game_id == game_id).all()
    
    if not progress:
        raise HTTPException(
            status_code=404, 
            detail="No progress found for this game."  
        )
    
    return progress

@router.put("/{progress_id}")
async def update_progress(
    progress_id: int,
    progress: schemas.ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing progress entry."""
    existing_progress = db.query(Progress).filter(Progress.id == progress_id).first()
    
    if not existing_progress:
        raise HTTPException(
            status_code=404, 
            detail="Progress entry not found."  
        )
    
    existing_progress.progress_percentage = progress.progress_percentage
    existing_progress.last_played_at = progress.last_played_at
    
    db.commit()
    db.refresh(existing_progress)
    
    return {
        "message": "Progress updated successfully.",
        "data": progress.model_dump()  # Corrigido de .dict() para .model_dump()
    }

@router.delete("/{progress_id}")
async def delete_progress(
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a progress entry."""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    
    if not progress:
        raise HTTPException(
            status_code=404, 
            detail="Progress entry not found."  
        )
    
    db.delete(progress)
    db.commit()
    
    return {
        "message": "Progress deleted successfully.",
        "data": progress.id
    }