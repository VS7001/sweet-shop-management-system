from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RegisterRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Sweet Shop Backend is running"}

@app.post("/api/auth/register", status_code=201)
def register_user(data: RegisterRequest):
    return {
        "email": data.email
    }
