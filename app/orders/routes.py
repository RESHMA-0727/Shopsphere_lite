from fastapi import APIRouter, Depends
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

# ADD TO CART
@router.post("/add")
def add_to_cart(product_id: int, quantity: int,
                db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return {"error": "Product not found"}

    item = models.Cart(username=user, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()

    return {"message": "Item added to cart", "product_id": product_id, "quantity": quantity}

# VIEW CART
@router.get("/")
def view_cart(db: Session = Depends(get_db),
              user: str = Depends(get_current_user)):

    if not user:
        return {"error": "Unauthorized"}

    items = db.query(models.Cart).filter(models.Cart.username == user).all()
    return {"cart_items": items}

# UPDATE CART ITEM
@router.put("/update")
def update_cart(product_id: int, quantity: int,
                db: Session = Depends(get_db),
                user: str = Depends(get_current_user)):

    item = db.query(models.Cart).filter(
        models.Cart.username == user,
        models.Cart.product_id == product_id
    ).first()

    if not item:
        return {"error": "Item not found in cart"}

    item.quantity = quantity
    db.commit()

    return {"message": "Cart updated successfully!!"}

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
