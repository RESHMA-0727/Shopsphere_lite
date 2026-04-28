from fastapi import FastAPI
from app.database import engine
from app import models

# Routers
from app.auth.routes import router as auth_router
from app.auth.profile import router as profile_router
from app.products.routes import router as product_router
from app.products.review_routes import router as review_router
from app.orders.routes import router as cart_router
from app.orders.order_routes import router as order_router
from app.orders.wishlist import router as wishlist_router

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(wishlist_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "ShopSphere Lite API Running Successfully 🚀"}
