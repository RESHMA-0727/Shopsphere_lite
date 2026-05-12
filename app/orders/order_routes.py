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

# PLACE ORDER
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

        if product.stock < item.quantity:
            return {"error": f"Not enough stock for product {product.name}"}

        # Reduce stock
        product.stock -= item.quantity

        order = models.Order(
            username=user,
            product_id=item.product_id,
            quantity=item.quantity,
            status="Pending"
        )

        db.add(order)

    db.commit()

    # Clear cart
    db.query(models.Cart).filter(models.Cart.username == user).delete()
    db.commit()

    logger.info(f"Order placed by user: {user}")

    return {"message": "Order placed successfully"}

# GET ORDERS
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
            "order_id": order.id,
            "product_name": product.name if product else "Unknown",
            "quantity": order.quantity,
            "status": order.status,
            "price": product.price if product else 0,
            "total": (product.price * order.quantity) if product else 0
        })

    return result

# UPDATE ORDER STATUS
@router.put("/update-status")
def update_order_status(order_id: int,
                        status: str,
                        db: Session = Depends(get_db),
                        user: str = Depends(get_current_user)):

    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.username == user
    ).first()

    if not order:
        return {"error": "Order not found"}

    order.status = status
    db.commit()

    logger.info(f"Order {order_id} updated to {status}")

    return {"message": f"Order status updated to {status}"}

# CANCEL ORDER
@router.post("/cancel")
def cancel_order(order_id: int,
                 db: Session = Depends(get_db),
                 user: str = Depends(get_current_user)):

    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.username == user
    ).first()

    if not order:
        return {"error": "Order not found"}

    product = db.query(models.Product).filter(
        models.Product.id == order.product_id
    ).first()

    # Restore stock
    if product:
        product.stock += order.quantity

    db.delete(order)
    db.commit()

    logger.info(f"Order cancelled by {user}")

    return {"message": "Order cancelled and stock restored"}
