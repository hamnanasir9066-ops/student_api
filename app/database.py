from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
MYSQL_USER="root"
MYSQL_PASSWORD="12345"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_DATABASE="fastapi_db"


DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()