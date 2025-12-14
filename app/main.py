from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta

from .database import SessionLocal, engine, Base
from .models import User, Sweet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# ---------- REQUEST MODELS ----------

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SweetCreateRequest(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

class SweetUpdateRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# ---------- ROUTES ----------

@app.get("/")
def root():
    return {"message": "Sweet Shop Backend is running"}

# ---------- AUTH ----------

@app.post("/api/auth/register", status_code=201)
def register_user(data: RegisterRequest):
    db = SessionLocal()

    if db.query(User).filter(User.email == data.email).first():
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(email=data.email, password=data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {"email": user.email}


@app.post("/api/auth/login")
def login_user(data: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()

    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    db.close()

    return {"access_token": token, "token_type": "bearer"}

# ---------- SWEETS ----------

@app.post("/api/sweets", status_code=201)
def add_sweet(data: SweetCreateRequest):
    db = SessionLocal()

    sweet = Sweet(
        name=data.name,
        category=data.category,
        price=data.price,
        quantity=data.quantity
    )

    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    db.close()

    return sweet


@app.get("/api/sweets")
def list_sweets():
    db = SessionLocal()
    sweets = db.query(Sweet).all()
    db.close()
    return sweets


@app.get("/api/sweets/search")
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    db = SessionLocal()
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    results = query.all()
    db.close()
    return results


@app.put("/api/sweets/{sweet_id}")
def update_sweet(sweet_id: int, data: SweetUpdateRequest):
    db = SessionLocal()

    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        db.close()
        raise HTTPException(status_code=404, detail="Sweet not found")

    if data.name is not None:
        sweet.name = data.name
    if data.category is not None:
        sweet.category = data.category
    if data.price is not None:
        sweet.price = data.price
    if data.quantity is not None:
        sweet.quantity = data.quantity

    db.commit()
    db.refresh(sweet)
    db.close()

    return sweet


@app.delete("/api/sweets/{sweet_id}", status_code=204)
def delete_sweet(sweet_id: int):
    db = SessionLocal()
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        db.close()
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(sweet)
    db.commit()
    db.close()


# ---------- INVENTORY ----------

@app.post("/api/sweets/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int):
    db = SessionLocal()
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        db.close()
        raise HTTPException(status_code=404, detail="Sweet not found")

    if sweet.quantity <= 0:
        db.close()
        raise HTTPException(status_code=400, detail="Out of stock")

    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)
    db.close()
    return sweet


@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(sweet_id: int):
    db = SessionLocal()
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if not sweet:
        db.close()
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.quantity += 1
    db.commit()
    db.refresh(sweet)
    db.close()
    return sweet
