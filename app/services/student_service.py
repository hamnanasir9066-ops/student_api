from sqlalchemy.orm import Session

from .. import models, schemas


def get_all_students(db: Session):
    return db.query(models.Student).all()


def get_student_by_id(student_id: int, db: Session):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def create_student(student_data: schemas.StudentCreate, db: Session):
    new_student = models.Student(
        id=student_data.id,
        name=student_data.name,
        department=student_data.department,
        semester=student_data.semester,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(student_id: int, updated_student: schemas.StudentCreate, db: Session):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return None

    student.name = updated_student.name
    student.department = updated_student.department
    student.semester = updated_student.semester

    db.commit()
    db.refresh(student)

    return student


def delete_student(student_id: int, db: Session):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return True
