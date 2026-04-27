from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

# USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)


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

# ORDER MODEL
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    product_id = Column(Integer)
    quantity = Column(Integer)

# Stores user wishlist items
class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    product_id = Column(Integer)
