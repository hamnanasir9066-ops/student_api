# Student API

This project is a FastAPI application that provides a RESTful API for managing student data. It allows users to perform CRUD (Create, Read, Update, Delete) operations on student records.

## Project Structure

```
student-api
├── app
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── main.py              # Entry point of the FastAPI application
│   ├── models.py            # Defines the database models using SQLAlchemy
│   ├── schemas.py           # Defines Pydantic schemas for data validation and serialization
│   ├── database.py          # Handles database connection and session management
│   └── routers
│       └── students.py      # Contains routes for handling student-related requests
├── requirements.txt         # Lists the dependencies required for the project
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd student-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

- **Get all students:** `GET /students`
- **Get a student by ID:** `GET /students/{student_id}`
- **Add a new student:** `POST /students`
- **Update an existing student:** `PUT /students/{student_id}`
- **Delete a student:** `DELETE /students/{student_id}`

## Dependencies

- FastAPI
- SQLAlchemy
- Uvicorn (for running the application)

## License

This project is licensed under the MIT License.