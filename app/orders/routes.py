from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/cart")

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD TO CART
@router.post("/add")
def add_to_cart(username: str, product_id: int, quantity: int, db: Session = Depends(get_db)):
    item = models.Cart(username=username, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    return {"message": "Item added to cart"}

# VIEW CART
@router.get("/")
def view_cart(username: str, db: Session = Depends(get_db)):
    items = db.query(models.Cart).filter(models.Cart.username == username).all()
    return items
