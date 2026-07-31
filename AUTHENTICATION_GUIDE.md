# FastAPI Authentication & Authorization Guide (Step-by-Step)

Iss document mein poori details ke sath samjhaaya gaya hai ke is Student Management API project mein Authentication (JWT Token) aur Password Hashing kis tarah implement ki gayi hai aur har file ka kya role hai.

---

## 🏗️ Overview of Authentication Flow

```
[ Client / Swagger UI ]
       │
       │  1. POST /auth/login (username & password)
       ▼
[ app/routers/auth.py ]
       │
       │  2. Calls authenticate_user()
       ▼
[ app/services/auth_service.py ] ──► Verifies password using [ app/utils/security.py ]
       │
       │  3. Generates JWT Access Token
       ▼
[ Client receives JWT Token ] (e.g. "eyJhbGciOiJIUzI1...")
       │
       │  4. Requests Protected Route (e.g. GET /users/me) with Header:
       │     Authorization: Bearer <token>
       ▼
[ app/utils/oauth2.py ] ──► Decodes token via [ app/utils/security.py ] & fetches User from DB
       │
       │  5. Injects current_user into Route
       ▼
[ Endpoint Response ]
```

---

## 📁 File-by-File Detailed Explanation

### 1. `app/config.py` (Centralized Configuration)
* **Purpose:** Application ki secret keys aur configuration settings ko manage karta hai.
* **Key Components:**
  * `SECRET_KEY`: JWT token ko sign (encrypt) aur verify karne ke liye unique key.
  * `ALGORITHM = "HS256"`: HMAC-SHA256 algorithm JWT generation ke liye.
  * `ACCESS_TOKEN_EXPIRE_MINUTES = 30`: Token 30 minutes tak valid rahega.

---

### 2. `app/utils/security.py` (Password Hashing & JWT Core Utility)
* **Purpose:** Passwords ko securely hash karna aur JWT tokens create/decode karna.
* **Key Functions:**
  * `pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")`: Password hashing engine configuration. We use `pbkdf2_sha256` which is built-in with Python's `hashlib` to ensure cross-platform compatibility (works without C/Rust compilers).
  * `hash_password(password: str) -> str`: Plain-text password (e.g., `"12345678"`) ko secure hash string mein convert karta hai DB mein store hone se pehle.
  * `verify_password(plain_password: str, hashed_password: str) -> bool`: Login ke waqt enter kiya hua plain password aur DB mein stored hash ko match karta hai.
  * `create_access_token(data: dict, expires_delta: Optional[timedelta]) -> str`: User payload (`sub` / user_id, `email`, `role`) aur expiration time (`exp`) ko pack karke JWT string generate karta hai.
  * `decode_access_token(token: str) -> Optional[dict]`: Request ke sath aaye hue JWT token ko decode aur verify karta hai. Agar valid ho toh payload dict return karta hai, warna `None`.

---

### 3. `app/schemas/auth.py` (Pydantic Models for Authentication)
* **Purpose:** Login aur Token response ke data structure ko define karta hai.
* **Key Models:**
  * `Token`: Login response ka format:
    ```json
    {
      "access_token": "eyJhbG...",
      "token_type": "bearer"
    }
    ```
  * `TokenData`: Token ke decoded payload mein maujood fields (`user_id`, `email`, `role`).

---

### 4. `app/services/auth_service.py` (Authentication Business Logic)
* **Purpose:** User validation aur token generation ki business logic handle karta hai.
* **Key Function:**
  * `authenticate_user(db: Session, credentials: OAuth2PasswordRequestForm)`:
    1. User ko email ya username se database mein search karta hai.
    2. Agar user na mile ➔ `401 Unauthorized` return karta hai.
    3. User milne par `verify_password()` ke zariye password match karta hai. Agar wrong password ho ➔ `401 Unauthorized` return karta hai.
    4. Account active hai ya nahi yeh check karta hai.
    5. User ki ID (`sub`), email, aur role include karke `create_access_token()` se JWT Token generate karta hai.
    6. Client ko `Token` schema ke mutabiq return kar deta hai.

---

### 5. `app/routers/auth.py` (Authentication API Endpoint)
* **Purpose:** `/auth/login` HTTP endpoint expose karta hai.
* **Key Endpoint:**
  * `POST /auth/login`:
    * Accepts form-data (`OAuth2PasswordRequestForm` containing `username` and `password`).
    * `auth_service.authenticate_user()` ko call karke Token return karta hai.
    * Swagger UI mein login button isi endpoint se connect hota hai.

---

### 6. `app/utils/oauth2.py` (Route Protection & Dependency Injection)
* **Purpose:** Protected routes par incoming requests ki authentication check karna aur Current User profile fetch karna.
* **Key Components:**
  * `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")`: Request Header (`Authorization: Bearer <token>`) se JWT Token auto-extract karta hai.
  * `get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User`:
    1. Header se token retrieve karta hai.
    2. `decode_access_token(token)` run karke token verify karta hai.
    3. Token se `user_id` (`sub`) extract karta hai.
    4. Database se matching `User` record fetch karta hai.
    5. Active check karta hai aur authenticated `User` object route function ko provide kar deta hai.
  * `RoleChecker`: Role-Based Access Control (RBAC) class dependency. Specific roles (e.g. `ADMIN`, `TEACHER`) ko specific routes permit ya deny karne ke liye istemal hoti hai.

---

### 7. `app/services/user_service.py` (User Creation with Hashing)
* **Purpose:** Users ki creation aur management.
* **Key Logic in User Creation:**
  * When a new user signs up / is created (`create_user()`):
    ```python
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),  # Hashing applied here!
        role=user.role,
        is_active=True
    )
    ```
  * Password plaintext store hone ki bajaye automatically hash ho kar DB mein save hota hai.

---

### 8. Protected Endpoints Usage Example (`app/routers/user.py` & `app/routers/students.py`)

#### Fetch Current Logged-In User Profile (`GET /users/me`):
```python
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

#### Admin/Teacher Only Route Example (`POST /students/`):
```python
allow_admin_or_teacher = RoleChecker([UserRole.ADMIN, UserRole.TEACHER])

@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_or_teacher)  # Protection applied!
):
    return student_service.create_student(student, db)
```

---

## 🔒 Summary of Security Principles Implemented

1. **Passwords are Never Stored as Plaintext:** Always hashed using `pbkdf2_sha256` in `security.py`.
2. **Stateless Authentication:** JWT Tokens contain user identity and expiration, avoiding server session state storage.
3. **Decoupled Architecture:** Separation of Concerns across Models, Schemas, Routers, Services, and Utils.
4. **Role-Based Authorization:** Endpoints are protected dynamically based on user roles (`ADMIN`, `TEACHER`, `STUDENT`).
