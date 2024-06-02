from fastapi import FastAPI
from .models import userModel
from .routers import user, auth
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}