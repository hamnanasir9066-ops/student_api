from fastapi import FastAPI

from app.database import Base, engine

# Import Routers
from app.routers import (
    user,
    students,
    department,
    subject,
    attendance,
    mark,
    fee,
    student_subject
)

# ==========================================
# Create Database Tables
# ==========================================

Base.metadata.create_all(bind=engine)

# ==========================================
# Create FastAPI App
# ==========================================

app = FastAPI(
    title="Student Management System API",
    description="A Professional Student Management System built with FastAPI",
    version="1.0.0"
)

# ==========================================
# Include Routers
# ==========================================

app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    students.router,
    prefix="/students",
    tags=["Students"]
)

app.include_router(
    department.router,
    prefix="/departments",
    tags=["Departments"]
)

app.include_router(
    subject.router,
    prefix="/subjects",
    tags=["Subjects"]
)

app.include_router(
    attendance.router,
    prefix="/attendance",
    tags=["Attendance"]
)

app.include_router(
    mark.router,
    prefix="/marks",
    tags=["Marks"]
)

app.include_router(
    fee.router,
    prefix="/fees",
    tags=["Fees"]
)

app.include_router(
    student_subject.router,
    prefix="/enrollments",
    tags=["Enrollments"]
)

# ==========================================
# Root Endpoint
# ==========================================

@app.get("/", tags=["Home"])
def root():
    return {
        "message": "Welcome to Student Management System API 🚀",
        "docs": "/docs",
        "redoc": "/redoc"
    }