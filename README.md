# 🛍️ ShopSphere Lite - E-commerce Backend

## 🚀 Overview
ShopSphere Lite is a modular e-commerce backend built using FastAPI.  
It supports user authentication, product management, cart functionality, and order processing.

This project is designed in a scalable way, similar to microservices architecture.

---

## 🧠 Features Implemented

### 🔐 Authentication
- User Signup
- User Login
- Password hashing (SHA256)
- JWT Token generation

### 🛍️ Product Management
- Add new products
- View all products

### 🛒 Cart System
- Add items to cart
- View cart items

### 📦 Order System
- Place order from cart
- Automatically clears cart after order
- View order history

---

## 🗄️ Database Design

### Users Table
- id
- username
- password

### Products Table
- id
- name
- description
- price

### Cart Table
- id
- username
- product_id
- quantity

### Orders Table
- id
- username
- product_id
- quantity

---

## 🔗 API Endpoints

### 🔐 Auth
- POST `/signup`
- POST `/login`

### 🛍️ Products
- POST `/products/add`
- GET `/products/`

### 🛒 Cart
- POST `/cart/add`
- GET `/cart/`

### 📦 Orders
- POST `/orders/place`
- GET `/orders/`

---

## ⚙️ Tech Stack
- FastAPI
- Python
- SQLite
- SQLAlchemy
- JWT (python-jose)

---

## ▶️ How to Run

```bash
cd shopsphere-lite
source venv/Scripts/activate
uvicorn app.main:app --reloadShopSphere Lite Backend Project
