from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.enums.user_role import UserRole
from app.utils.security import hash_password


def create_default_admin():
    db: Session = SessionLocal()

    try:
        admin = db.query(User).filter(
            User.role == UserRole.ADMIN
        ).first()

        if admin:
            print("Default admin already exists.")
            return

        default_admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("Admin@123"),
            role=UserRole.ADMIN,
            is_active=True
        )

        db.add(default_admin)
        db.commit()

        print("Default admin created successfully!")

    finally:
        db.close()