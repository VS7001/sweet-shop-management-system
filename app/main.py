from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

# in-memory storage (will be replaced by DB later)
app.state.users = []
app.state.sweets = []


# JWT config (simple for assignment)
SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# --------- Request Models ---------

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SweetRequest(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


# --------- Routes ---------

@app.get("/")
def root():
    return {"message": "Sweet Shop Backend is running"}

# --------- Register ---------

@app.post("/api/auth/register", status_code=201)
def register_user(data: RegisterRequest):
    for user in app.state.users:
        if user["email"] == data.email:
            raise HTTPException(status_code=400, detail="User already exists")

    app.state.users.append({
        "email": data.email,
        "password": data.password
    })

    return {
        "email": data.email
    }

# --------- Login + JWT ---------

@app.post("/api/auth/login")
def login_user(data: LoginRequest):
    for user in app.state.users:
        if user["email"] == data.email and user["password"] == data.password:
            payload = {
                "sub": data.email,
                "exp": datetime.utcnow() + timedelta(minutes=30)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/sweets", status_code=201)
def add_sweet(data: SweetRequest):
    sweet = {
        "id": len(app.state.sweets) + 1,
        "name": data.name,
        "category": data.category,
        "price": data.price,
        "quantity": data.quantity
    }

    app.state.sweets.append(sweet)
    return sweet


@app.get("/api/sweets")
def list_sweets():
    return app.state.sweets


@app.get("/api/sweets/search")
def search_sweets(name: str | None = None):
    results = app.state.sweets

    if name:
        results = [s for s in results if s["name"].lower() == name.lower()]

    return results

@app.post("/api/sweets/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int):
    for sweet in app.state.sweets:
        if sweet["id"] == sweet_id:
            if sweet["quantity"] <= 0:
                raise HTTPException(status_code=400, detail="Out of stock")

            sweet["quantity"] -= 1
            return sweet

    raise HTTPException(status_code=404, detail="Sweet not found")


@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(sweet_id: int):
    for sweet in app.state.sweets:
        if sweet["id"] == sweet_id:
            sweet["quantity"] += 1
            return sweet

    raise HTTPException(status_code=404, detail="Sweet not found")
