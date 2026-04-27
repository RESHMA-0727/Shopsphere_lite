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
    if not name.strip():
        return {"error": "Product name cannot be empty"}

    if price <= 0:
        return {"error": "Price must be greater than zero"}

    product = models.Product(name=name, description=description, price=price)
    db.add(product)
    db.commit()

    return {"message": "Product added successfully!!"}

# GET ALL PRODUCTS (CLEAN RESPONSE)
@router.get("/")
def get_products(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price
        }
        for p in products
    ]

# GET PRODUCT BY ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price
    }

# SEARCH PRODUCTS
@router.get("/search")
def search_products(name: str, db: Session = Depends(get_db)):
    results = db.query(models.Product).filter(models.Product.name.contains(name)).all()

    return [
        {"id": p.id, "name": p.name, "price": p.price}
        for p in results
    ]

# FILTER PRODUCTS
@router.get("/filter")
def filter_products(min_price: int, max_price: int, db: Session = Depends(get_db)):
    results = db.query(models.Product).filter(
        models.Product.price >= min_price,
        models.Product.price <= max_price
    ).all()

    return [
        {"id": p.id, "name": p.name, "price": p.price}
        for p in results
    ]
