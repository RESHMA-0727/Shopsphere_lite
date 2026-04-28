from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.routes import get_current_user
from app import models
from app.logger import logger

router = APIRouter(prefix="/cart")

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD TO CART (NO DUPLICATES)
@router.post("/add")
def add_to_cart(product_id: int, quantity: int,
                db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    existing_item = db.query(models.Cart).filter(
        models.Cart.username == user,
        models.Cart.product_id == product_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
        db.commit()

        logger.info(f"Updated cart item for {user}, product {product_id}")

        return {"message": "Cart updated"}

    item = models.Cart(
        username=user,
        product_id=product_id,
        quantity=quantity
    )

    db.add(item)
    db.commit()

    logger.info(f"Added to cart: {user}, product {product_id}")

    return {"message": "Added to cart"}

# VIEW CART
@router.get("/")
def view_cart(db: Session = Depends(get_db),
              user: str = Depends(get_current_user)):

    items = db.query(models.Cart).filter(models.Cart.username == user).all()

    return items

# UPDATE CART
@router.put("/update")
def update_cart(product_id: int, quantity: int,
                db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    item = db.query(models.Cart).filter(
        models.Cart.username == user,
        models.Cart.product_id == product_id
    ).first()

    if not item:
        return {"error": "Item not found"}

    item.quantity = quantity
    db.commit()

    return {"message": "Cart updated"}

# DELETE FROM CART
@router.delete("/delete")
def delete_from_cart(product_id: int,
                     db: Session = Depends(get_db),
                     user: str = Depends(get_current_user)):

    item = db.query(models.Cart).filter(
        models.Cart.username == user,
        models.Cart.product_id == product_id
    ).first()

    if not item:
        return {"error": "Item not found"}

    db.delete(item)
    db.commit()

    return {"message": "Item removed from cart"}
