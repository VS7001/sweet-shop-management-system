from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

app.state.users = []

class RegisterRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Sweet Shop Backend is running"}

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
