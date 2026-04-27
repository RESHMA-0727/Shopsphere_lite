from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import hashlib
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()

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

# GET CURRENT USER (UPDATED)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]

# SIGNUP

@router.post("/signup")
def signup(username: str, password: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()

    if existing_user:
        return {"error": "Username already exists"}

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = models.User(username=username, password=hashed_password, email=email)
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

    token = create_access_token({"sub": user.username})
    return {"access_token": token}
