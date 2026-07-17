from pydantic import BaseModel


# Used when creating a new student
class StudentCreate(BaseModel):
    id: int
    name: str
    department: str
    semester: int


# Used when returning student data
class StudentResponse(BaseModel):
    id: int
    name: str
    department: str
    semester: int

    class Config:
        from_attributes = True