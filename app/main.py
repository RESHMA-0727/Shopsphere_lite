from fastapi import FastAPI
from app.database import engine
from app import models
from app.auth.routes import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "ShopSphere Lite API Running Sucessfuly !!🚀"}





