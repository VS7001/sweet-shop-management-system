# 🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built using **FastAPI**, **SQLite**, and a simple **HTML/CSS/JavaScript** frontend.  
The project follows **Test-Driven Development (TDD)** principles and demonstrates clean API design, authentication, role-based access control, and modern development workflows.

---

## 📌 Objective

The goal of this project is to design, build, and test a Sweet Shop Management System that allows:

- Users to register and log in  
- Customers to browse and purchase sweets  
- Admins to manage sweets and inventory  
- Searching sweets using multiple filters  
- Reliable backend backed by a real database  
- High test coverage using TDD practices  

---

## 🧱 Tech Stack

### Backend
- Python  
- FastAPI  
- SQLAlchemy  
- SQLite  
- JWT (JSON Web Tokens)  

### Frontend
- HTML  
- CSS  
- Vanilla JavaScript  

### Testing
- pytest  
- FastAPI TestClient  

### Tools
- Git & GitHub  
- VS Code  

---

## ✨ Features Implemented

### 🔐 Authentication
- User registration  
- User login  
- JWT-based authentication  
- Role-based access (`user`, `admin`)  

### 🍭 Sweets Management
- Add new sweets (Admin)  
- View all sweets (Public)  
- Update sweet details (Admin)  
- Delete sweets (Admin)  
- Purchase sweets (Authenticated user)  
- Restock sweets (Admin)  

### 🔎 Search & Filter
- Search by name  
- Filter by category  
- Filter by price range (min / max)  

### 📦 Inventory Management
- Automatic quantity reduction on purchase  
- Manual restocking by admin  

---

## 🔑 User Roles

| Role  | Permissions |
|------|-------------|
| User | View sweets, search sweets, purchase sweets |
| Admin | Add sweets, update sweets, delete sweets, restock |

> By default, users register with role `user`.  
> Admin users can be created by passing `"role": "admin"` during registration.

---

## 🧪 Test-Driven Development (TDD)

This project follows the **Red → Green → Refactor** methodology.

### Test Coverage Includes:
- User registration  
- Duplicate registration handling  
- Login and JWT token generation  
- Sweet creation  
- Search functionality  
- Update & delete sweets  
- Inventory purchase & restock  

All tests pass successfully.

### Run tests:
```bash
pytest
```

---

## 🗄 Database

- SQLite is used as the persistent database  
- SQLAlchemy ORM is used for database interactions  
- In-memory storage is **not** used  

**Database file:**  
`sweetshop.db`

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VS7001/sweet-shop-management-system.git
cd sweet-shop-management-system
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Start Backend Server
```bash
uvicorn app.main:app --reload
```

Backend runs at:  
http://127.0.0.1:8000

### 5️⃣ Run Frontend

Open the following file in your browser:

`Frontend/index.html`

---

## 📡 API Endpoints Overview

### Auth
- POST `/api/auth/register`
- POST `/api/auth/login`

### Sweets
- GET `/api/sweets`
- GET `/api/sweets/search`
- POST `/api/sweets` (Admin)
- PUT `/api/sweets/{id}` (Admin)
- DELETE `/api/sweets/{id}` (Admin)

### Inventory
- POST `/api/sweets/{id}/purchase`
- POST `/api/sweets/{id}/restock` (Admin)

---

## 📸 Screenshots

### Login
![Login](screenshots/login.png)

### Register
![Register](screenshots/register.png)

### Dashboard – Add Sweet
![Dashboard](screenshots/dashboard.png)

### Search & Filters
![Search](screenshots/search.png)

### Sweet Added Successfully
![Sweet Added](screenshots/sweet-added.png)

### Sweets List (Update & Purchase)
![Sweets](screenshots/sweets-list.png)


---

## 🤖 My AI Usage

### Tools Used
- ChatGPT

### How I Used AI
- Clarifying FastAPI concepts and best practices  
- Understanding JWT structure and expiration handling  
- Debugging test failures and SQLAlchemy issues  
- Structuring API routes logically  
- Improving readability and maintainability of code  

### Reflection
AI was used as a supporting tool, not a replacement for understanding.  
All logic was reviewed, modified, and integrated manually.  
Architecture decisions, testing, and debugging were done consciously to ensure correctness and learning.

---

## 🏁 Conclusion

This project demonstrates:

- Clean backend architecture  
- Strong fundamentals in API design  
- Testing discipline  
- Responsible AI usage  
- End-to-end functionality  
