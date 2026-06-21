from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.models import Review, User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_review = Review(**review.model_dump())
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
    reviews = db.query(Review).filter(Review.game_id == game_id).all()
    return reviews

@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, 
                  review: schemas.ReviewUpdate, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
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
    
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}