from pydantic import BaseModel, EmailStr,field_validator, Field
from typing import Union, Optional, Literal
from src.models.user import UserRole

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    
    class Config:
        from_attributes = True
        
class Login(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    @field_validator('role')
    def validate_role(cls, v):
        if v not in UserRole.__members__.values():
            raise ValueError('Invalid user role')
        return v

class StudentCreate(UserCreate):
    registration: str
    role: UserRole = UserRole.STUDENT


class TeacherCreate(UserCreate):
    specialization: str 
    role: UserRole = UserRole.TEACHER

class AdminCreate(UserCreate):
    role: UserRole = UserRole.ADMIN


class UserUpdateBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=1)
    
class StudentUpdate(UserUpdateBase):
    role: Literal["student"] = "student"
    registration: Optional[str] = Field(None, min_length=1)

class TeacherUpdate(UserUpdateBase):
    role: Literal["teacher"] = "teacher"
    specialization: Optional[str] = Field(None, min_length=1)



UserUpdate=Union[StudentUpdate, TeacherUpdate, UserUpdateBase]


class CourseBase(BaseModel):
    name: str
    video: str
    teacher_id: int
    
    
class RegistrationBase(BaseModel):
    student_id: int
    course_id: int