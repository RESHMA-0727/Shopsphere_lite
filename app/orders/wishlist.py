from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.routes import get_current_user
from app import models

router = APIRouter(prefix="/wishlist")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD TO WISHLIST
@router.post("/add")
def add_to_wishlist(product_id: int,
                    db: Session = Depends(get_db),
                    user: str = Depends(get_current_user)):

    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    item = models.Wishlist(username=user, product_id=product_id)
    db.add(item)
    db.commit()

    return {"message": "Added to wishlist"}

# VIEW WISHLIST
@router.get("/")
def view_wishlist(db: Session = Depends(get_db),
                  user: str = Depends(get_current_user)):

    items = db.query(models.Wishlist).filter(models.Wishlist.username == user).all()
    return items

# REMOVE FROM WISHLIST
@router.delete("/remove")
def remove_from_wishlist(product_id: int,
                        db: Session = Depends(get_db),
                        user: str = Depends(get_current_user)):

    item = db.query(models.Wishlist).filter(
        models.Wishlist.username == user,
        models.Wishlist.product_id == product_id
    ).first()

    if not item:
        return {"error": "Item not found"}

    db.delete(item)
    db.commit()

    return {"message": "Removed from wishlist"}
