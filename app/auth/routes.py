from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import hashlib

router = APIRouter()

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SIGNUP
@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    # hash password using sha256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # create user
    user = models.User(username=username, password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}

# LOGIN
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    # hash input password
    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    if not user or user.password != hashed_input:
        return {"error": "Invalid credentials"}

    return {"message": "Login successfull"}
