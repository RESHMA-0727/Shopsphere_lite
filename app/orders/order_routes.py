from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.auth.routes import get_current_user

router = APIRouter(prefix="/orders")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PLACE ORDER (PROTECTED)
@router.post("/place")
def place_order(db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    cart_items = db.query(models.Cart).filter(models.Cart.username == user).all()

    if not cart_items:
        return {"error": "Cart is empty"}

    for item in cart_items:
        order = models.Order(
            username=item.username,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order)

    db.query(models.Cart).filter(models.Cart.username == user).delete()
    db.commit()

    return {"message": "Order placed successfully"}

# VIEW ORDERS (PROTECTED)
@router.get("/")
def get_orders(db: Session = Depends(get_db),
               user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    orders = db.query(models.Order).filter(models.Order.username == user).all()
    return orders
