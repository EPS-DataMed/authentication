from fastapi import FastAPI
from . import models
from .routers import user, auth
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)