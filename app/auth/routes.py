from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import hashlib
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# SIGNUP
@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    
    if existing_user:
        return {"error": "Username already exists"}

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = models.User(username=username, password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}

# LOGIN
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    if not user or user.password != hashed_input:
        return {"error": "Invalid credentials"}

    # create JWT token
    token = create_access_token({"sub": user.username})

    return {"access_token": token}
