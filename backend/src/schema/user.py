from pydantic import BaseModel, EmailStr,field_validator, Field
from typing import Union, Optional, Literal
from src.models.user import UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

        
class Login(BaseModel):
    email: str
    password: str

class StudentCreate(UserBase):
    registration: str
    role: UserRole = UserRole.STUDENT


class TeacherCreate(UserBase):
    specialization: str 
    role: UserRole = UserRole.TEACHER

class AdminCreate(UserBase):
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
