from fastapi import FastAPI

from . import models
from .database import engine
from .routers import students

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI()
app.include_router(students.router, prefix="/students", tags=["students"])
