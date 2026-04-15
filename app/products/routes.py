from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/products")

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD PRODUCT
@router.post("/add")
def add_product(name: str, description: str, price: int, db: Session = Depends(get_db)):
    product = models.Product(name=name, description=description, price=price)
    db.add(product)
    db.commit()
    return {"message": "Product added successfully"}

# GET ALL PRODUCTS
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
