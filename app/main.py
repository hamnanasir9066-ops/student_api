from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI()


# -------------------- GET ALL STUDENTS --------------------

@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


# -------------------- GET STUDENT BY ID --------------------

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return {"message": "Student not found"}

    return student


# -------------------- ADD STUDENT --------------------

@app.post("/students", response_model=schemas.StudentResponse)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(
        id=student.id,
        name=student.name,
        department=student.department,
        semester=student.semester
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# -------------------- UPDATE STUDENT --------------------

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return {"message": "Student not found"}

    student.name = updated_student.name
    student.department = updated_student.department
    student.semester = updated_student.semester

    db.commit()
    db.refresh(student)

    return student


# -------------------- DELETE STUDENT --------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return {"message": "Student not found"}

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}