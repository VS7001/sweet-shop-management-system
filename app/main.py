from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

# in-memory storage (will be replaced by DB later)
app.state.users = []

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
