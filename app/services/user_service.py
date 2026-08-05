from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.student import Student
from app.models.department import Department

from app.schemas.user import UserCreate, UserUpdate

from app.enums.user_role import UserRole

from app.utils.security import hash_password


# ==========================================
# Get All Users
# ==========================================

def get_all_users(db: Session):
    return db.query(User).all()


# ==========================================
# Get User By ID
# ==========================================

def get_user_by_id(user_id: int, db: Session):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# Get User By Username
# ==========================================

def get_user_by_username(username: str, db: Session):

    return db.query(User).filter(
        User.username == username
    ).first()


# ==========================================
# Get User By Email
# ==========================================

def get_user_by_email(email: str, db: Session):

    return db.query(User).filter(
        User.email == email
    ).first()


# ==========================================
# Create User
# ==========================================

def create_user(user: UserCreate, db: Session):

    # Check username
    if get_user_by_username(user.username, db):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    if get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Validate Student Data
    if user.role == UserRole.STUDENT:

        required_fields = [
            user.first_name,
            user.last_name,
            user.roll_number,
            user.department_id,
            user.semester
        ]

        if any(field is None for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail="Student information is required."
            )

        department = db.query(Department).filter(
            Department.id == user.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        existing_roll = db.query(Student).filter(
            Student.roll_number == user.roll_number
        ).first()

        if existing_roll:
            raise HTTPException(
                status_code=400,
                detail="Roll number already exists"
            )

    # Create User
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_active=True
    )

    db.add(new_user)

    # Generate ID
    db.flush()

    # Automatically Create Student Profile
    if new_user.role == UserRole.STUDENT:

        student = Student(
            user_id=new_user.id,
            department_id=user.department_id,
            roll_number=user.roll_number,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            semester=user.semester,
            cgpa=user.cgpa if user.cgpa else 0.0,
            address=user.address
        )

        db.add(student)

    db.commit()

    db.refresh(new_user)

    return new_user


# ==========================================
# Update User
# ==========================================

def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session
):

    user = get_user_by_id(user_id, db)

    if updated_user.username is not None:

        existing = db.query(User).filter(
            User.username == updated_user.username,
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        user.username = updated_user.username

    if updated_user.email is not None:

        existing = db.query(User).filter(
            User.email == updated_user.email,
            User.id != user_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.email = updated_user.email

    if updated_user.password is not None:
        user.hashed_password = hash_password(updated_user.password)

    if updated_user.role is not None:
        user.role = updated_user.role

    if updated_user.is_active is not None:
        user.is_active = updated_user.is_active

    db.commit()
    db.refresh(user)

    return user


# ==========================================
# Delete User
# ==========================================

def delete_user(
    user_id: int,
    db: Session
):

    user = get_user_by_id(user_id, db)

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }


# ==========================================
# Change Password
# ==========================================

def change_user_password(
    user_id: int,
    new_password: str,
    db: Session
):

    user = get_user_by_id(user_id, db)

    user.hashed_password = hash_password(new_password)

    db.commit()

    db.refresh(user)

    return {
        "message": "Password updated successfully"
    }