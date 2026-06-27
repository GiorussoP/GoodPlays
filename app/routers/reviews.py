from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.models import Review, User
from app.routers.auth import get_current_user
from sqlalchemy.orm import selectinload
from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # Security Fix: Ignore user_id from payload and use the authenticated user's ID
    db_review = Review(
        user_id=current_user.id,
        game_id=review.game_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.now().isoformat()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{review_id}", response_model=schemas.ReviewResponse)
def get_review(review_id: int, 
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/game/{game_id}", response_model=List[schemas.ReviewResponse])
def get_game_reviews(game_id: int, 
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    reviews = db.query(Review).options(
        selectinload(Review.user)
    ).filter(Review.game_id == game_id).all()
    return reviews

@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, 
                  review: schemas.ReviewUpdate, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Security Fix: Check ownership
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    
    for key, value in review.model_dump(exclude_unset=True).items():
        setattr(db_review, key, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review

@router.delete("/{review_id}")
def delete_review(review_id: int, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Security Fix: Check ownership
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}

# Nova rota para obter o username do usuário atual
@router.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user