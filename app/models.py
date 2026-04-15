from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

# USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# PRODUCT MODEL
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

# CART MODEL
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
