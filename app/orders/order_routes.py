from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/orders")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PLACE ORDER
@router.post("/place")
def place_order(username: str, db: Session = Depends(get_db)):
    cart_items = db.query(models.Cart).filter(models.Cart.username == username).all()

    if not cart_items:
        return {"error": "Cart is empty"}

    # move cart items to orders
    for item in cart_items:
        order = models.Order(
            username=item.username,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order)

    # clear cart
    db.query(models.Cart).filter(models.Cart.username == username).delete()
    db.commit()

    return {"message": "Order placed successfully"}

# VIEW ORDERS
@router.get("/")
def get_orders(username: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.username == username).all()
    return orders
