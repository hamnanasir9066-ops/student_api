from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.department import Department
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate


def ensure_student_columns(db: Session):
    existing_columns = {
        row[0]
        for row in db.execute(text("SHOW COLUMNS FROM students")).fetchall()
    }

    column_definitions = {
        "user_id": "INT",
        "department_id": "INT",
        "roll_number": "VARCHAR(30)",
        "first_name": "VARCHAR(100)",
        "last_name": "VARCHAR(100)",
        "phone": "VARCHAR(20)",
        "gender": "VARCHAR(20)",
        "date_of_birth": "DATE",
        "semester": "INT",
        "cgpa": "FLOAT DEFAULT 0",
        "address": "VARCHAR(255)",
        "created_at": "DATETIME DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
    }

    for column_name, definition in column_definitions.items():
        if column_name not in existing_columns:
            db.execute(
                text(f"ALTER TABLE students ADD COLUMN {column_name} {definition}")
            )

    if "name" in existing_columns:
        db.execute(text("ALTER TABLE students DROP COLUMN name"))

    if "department" in existing_columns:
        db.execute(text("ALTER TABLE students DROP COLUMN department"))

    db.commit()


# ==========================================
# Get All Students
# ==========================================

def get_all_students(db: Session):
    return (
        db.query(Student)
        .join(User, User.id == Student.user_id)
        .filter(
            Student.first_name.isnot(None),
            Student.last_name.isnot(None),
            Student.department_id.isnot(None),
            Student.roll_number.isnot(None)
        )
        .all()
    )
# ==========================================
# Get Student By ID
# ==========================================

def get_student_by_id(student_id: int, db: Session):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ==========================================
# Create Student
# ==========================================

def create_student(student: StudentCreate, db: Session):

    ensure_student_columns(db)

    # Check duplicate roll number
    existing_student = db.query(Student).filter(
        Student.roll_number == student.roll_number
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Roll Number already exists"
        )

    # Check department exists
    department = db.query(Department).filter(
        Department.id == student.department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    new_student = Student(
        user_id=student.user_id,
        department_id=student.department_id,
        roll_number=student.roll_number,
        first_name=student.first_name,
        last_name=student.last_name,
        phone=student.phone,
        gender=student.gender,
        date_of_birth=student.date_of_birth,
        semester=student.semester,
        cgpa=student.cgpa,
        address=student.address
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ==========================================
# Update Student
# ==========================================

def update_student(
    student_id: int,
    updated_student: StudentUpdate,
    db: Session
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if updated_student.first_name is not None:
        student.first_name = updated_student.first_name

    if updated_student.last_name is not None:
        student.last_name = updated_student.last_name

    if updated_student.phone is not None:
        student.phone = updated_student.phone

    if updated_student.gender is not None:
        student.gender = updated_student.gender

    if updated_student.date_of_birth is not None:
        student.date_of_birth = updated_student.date_of_birth

    if updated_student.semester is not None:
        student.semester = updated_student.semester

    if updated_student.cgpa is not None:
        student.cgpa = updated_student.cgpa

    if updated_student.address is not None:
        student.address = updated_student.address

    if updated_student.user_id is not None:

        user_exists = db.query(User).filter(User.id == updated_student.user_id).first()
        if user_exists is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        existing_student = db.query(Student).filter(
            Student.user_id == updated_student.user_id,
            Student.id != student_id
        ).first()

        if existing_student is not None:
            raise HTTPException(
                status_code=400,
                detail="This user is already assigned to another student"
            )

        student.user_id = updated_student.user_id

    if updated_student.department_id is not None:

        department = db.query(Department).filter(
            Department.id == updated_student.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        student.department_id = updated_student.department_id

    db.commit()
    db.refresh(student)

    return student


# ==========================================
# Delete Student
# ==========================================

def delete_student(student_id: int, db: Session):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }


# ==========================================
# Get Student By User ID (Self-Service)
# ==========================================

def get_student_by_user_id(user_id: int, db: Session):
    """
    Retrieves the Student profile associated with a specific User ID.
    Raises HTTP 404 if no student profile exists for the user.
    """
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found for this user account"
        )
    return student
