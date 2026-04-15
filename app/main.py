from fastapi import FastAPI
from app.database import engine
from app import models
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.orders.routes import router as cart_router

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# include routes
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)

@app.get("/")
def home():
    return {"message": "ShopSphere Lite API Running Sucessfully !!🚀"}





