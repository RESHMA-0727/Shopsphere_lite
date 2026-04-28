from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.routes import get_current_user
from app import models
from app.logger import logger

router = APIRouter(prefix="/orders")

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PLACE ORDER (WITH STOCK VALIDATION)
@router.post("/place")
def place_order(db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    cart_items = db.query(models.Cart).filter(models.Cart.username == user).all()

    if not cart_items:
        return {"error": "Cart is empty"}

    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

        if not product:
            return {"error": f"Product {item.product_id} not found"}

        # ❌ STOCK CHECK
        if product.stock < item.quantity:
            return {"error": f"Not enough stock for product {product.name}"}

        # ✅ REDUCE STOCK
        product.stock -= item.quantity

        order = models.Order(
            username=user,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order)

    db.commit()

    # CLEAR CART
    db.query(models.Cart).filter(models.Cart.username == user).delete()
    db.commit()

    logger.info(f"Order placed by user: {user}")

    return {"message": "Order placed successfully"}

# GET ORDER HISTORY
@router.get("/")
def get_orders(db: Session = Depends(get_db),
               user: str = Depends(get_current_user)):

    orders = db.query(models.Order).filter(models.Order.username == user).all()

    if not orders:
        return {"message": "No orders found"}

    result = []

    for order in orders:
        product = db.query(models.Product).filter(models.Product.id == order.product_id).first()

        result.append({
            "product_name": product.name if product else "Unknown",
            "quantity": order.quantity,
            "price": product.price if product else 0,
            "total": (product.price * order.quantity) if product else 0
        })

    logger.info(f"Fetched order history for user: {user}")

    return result
