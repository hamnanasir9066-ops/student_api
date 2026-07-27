# 🎓 Student Management System API

A comprehensive, production-ready RESTful API built with **FastAPI**, **SQLAlchemy**, and **MySQL** for managing educational institutions. The API supports full management of Users, Students, Departments, Subjects, Course Enrollments, Attendance Records, Academic Marks, and Fee Management.

---

## 🌟 Key Features

### 👤 1. User Management (`/users`)
- Role-based user creation (`admin`, `teacher`, `student`).
- Password hashing with `passlib[bcrypt]`.
- User activation, updates, and profile management.

### 🎓 2. Student Management (`/students`)
- Manage detailed student profiles (Roll Number, Semester, CGPA, Address, Contact).
- Associate students with specific Departments and User accounts.

### 🏢 3. Department Management (`/departments`)
- Manage academic departments, department codes, and Head of Department (HOD) details.

### 📚 4. Subject Management (`/subjects`)
- Create and manage academic subjects/courses with credit hours and department links.

### 📝 5. Course Enrollments (`/enrollments`)
- Enroll students in specific subjects.
- Prevent duplicate subject enrollments per student.

### 📅 6. Attendance Tracking (`/attendance`)
- Log and track daily student attendance per subject (`Present`, `Absent`, `Leave`).

### 📊 7. Marks & Grading (`/marks`)
- Log academic evaluation metrics (Quizzes, Assignments, Midterms, Finals).
- Automatic calculation of total score and letter grades (`A+`, `A`, `B`, `C`, `D`, `F`).

### 💳 8. Fee Management (`/fees`)
- Track tuition and fee structures, due dates, paid dates, and status (`PENDING`, `PAID`, `OVERDUE`).

---

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Driver**: [PyMySQL](https://pymysql.readthedocs.io/)
- **Database**: MySQL
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Authentication & Hashing**: [Passlib](https://passlib.readthedocs.io/), [Python-Jose](https://python-jose.readthedocs.io/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Project Structure

```text
student_api/
├── app/
│   ├── enums/                # Enumerations (AttendanceStatus, FeeStatus, Grade)
│   ├── models/               # SQLAlchemy ORM Database Models
│   ├── routers/              # API Route Handlers (FastAPI APIRouter)
│   ├── schemas/              # Pydantic Schemas & Data Validation
│   ├── services/             # Business Logic & Database Layer
│   └── database.py           # Database Configuration & Session Setup
├── main.py                   # FastAPI Application Entrypoint
├── requirements.txt          # Python Project Dependencies
└── README.md                 # Project Documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL Server running locally or remotely

### 1. Clone the Repository
```bash
git clone https://github.com/hamnanasir9066-ops/student_api.git
cd student_api
```

### 2. Activate Virtual Environment
- **PowerShell**:
  ```powershell
  .\venv\bin\Activate.ps1
  ```
- **Git Bash / Bash**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Configure your MySQL connection details in `app/database.py`:
```python
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "fastapi_db"
```

### 5. Run the Server
```bash
python -m uvicorn main:app --reload
```

---

## 📖 API Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)