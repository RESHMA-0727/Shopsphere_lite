# 🛍️ ShopSphere Lite - E-commerce Backend

## 🚀 Overview
ShopSphere Lite is a modular e-commerce backend built using FastAPI.  
It simulates a real-world online shopping system with authentication, product management, cart functionality, and order processing.

---

## 🧠 Architecture

The system is divided into modules:

- 🔐 Auth Module → Signup, Login, JWT Authentication  
- 🛍️ Product Module → Product management and search  
- 🛒 Cart Module → Cart operations  
- 📦 Order Module → Order processing  

Designed with a scalable structure similar to microservices.

---

## 🧩 Features

### 🔐 Authentication
- User Signup & Login
- Password hashing (SHA256)
- JWT Token authentication
- Protected APIs

---

### 🛍️ Product Service (Week 2)
- Add products
- View all products
- Get product by ID
- Search products by name
- Filter products by price
- Input validation
- Clean API responses

---

### 🛒 Cart System
- Add to cart
- View cart
- Update quantity
- Remove item

---

### 📦 Order System
- Place order from cart
- Calculate total price
- Clear cart after order
- View orders

---

## 🗄️ Database Schema

### Users
- id, username, password

### Products
- id, name, description, price

### Cart
- id, username, product_id, quantity

### Orders
- id, username, product_id, quantity

---

## 🔗 API Endpoints

### Auth
- POST `/signup`
- POST `/login`

### Products
- POST `/products/add`
- GET `/products/`
- GET `/products/{id}`
- GET `/products/search`
- GET `/products/filter`

### Cart
- POST `/cart/add`
- GET `/cart/`
- PUT `/cart/update`
- DELETE `/cart/delete`

### Orders
- POST `/orders/place`
- GET `/orders/`

---

## ⚙️ Tech Stack
- FastAPI
- Python
- SQLite
- SQLAlchemy
- JWT

---

## ▶️ Run Project

```bash
cd shopsphere-lite
source venv/Scripts/activate
uvicorn app.main:app --reload
