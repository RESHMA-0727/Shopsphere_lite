from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.routes import get_current_user
from app import models

router = APIRouter(prefix="/profile")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET USER PROFILE
@router.get("/")
def get_profile(db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    user_data = db.query(models.User).filter(models.User.username == user).first()

    if not user_data:
        return {"error": "User not found"}

    return {
        "username": user_data.username,
        "email": user_data.email
    }
