# ShopSphere Lite - E-commerce Backend

## 🚀 Overview
A modular e-commerce backend built using FastAPI.  
Implements core functionalities like authentication, product management, and cart system.

---

## 🧠 Architecture
The system is structured in a modular way (microservice-ready design):

- Auth Module (User Signup/Login + JWT)
- Product Module (Product Catalog)
- Cart Module (Cart Management)

---

## 🗄️ Database Schema

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

---

## 🔗 API Endpoints

### 🔐 Auth
- POST /signup
- POST /login

### 🛍️ Products
- POST /products/add
- GET /products/

### 🛒 Cart
- POST /cart/add
- GET /cart/

---

## ⚙️ Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication

---

## ▶️ How to Run

```bash
source venv/Scripts/activate
uvicorn app.main:app --reload
