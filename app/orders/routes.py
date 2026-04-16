from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth.routes import get_current_user

router = APIRouter(prefix="/cart")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD TO CART (PROTECTED)
@router.post("/add")
def add_to_cart(product_id: int, quantity: int,
                db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    item = models.Cart(username=user, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()

    return {"message": "Item added to cart"}

# VIEW CART (PROTECTED)
@router.get("/")
def view_cart(db: Session = Depends(get_db),
              user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    items = db.query(models.Cart).filter(models.Cart.username == user).all()
    return items
