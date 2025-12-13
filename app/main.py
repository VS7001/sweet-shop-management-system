from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sweet Shop Backend is running"}
