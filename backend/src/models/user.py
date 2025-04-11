from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database.session import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole))

    __mapper_args__ = {
        "polymorphic_identity": "users",
        "polymorphic_on": role
    }


class Student(User):
    __tablename__ = "students"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    registration = Column(String(50), unique=True, nullable=False)
    enrolled_courses = relationship("Registration", back_populates="student")
    
    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

class Teacher(User):
    __tablename__ = "teachers"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    specialization = Column(String(100), nullable=False)
    courses = relationship("Course", back_populates="teacher")
    
    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }

class Admin(User):
    __tablename__ = "admins"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    video = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="courses")
    registrations = relationship("Registration", back_populates="courses") 
    

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    student = relationship("Student", back_populates="enrolled_courses")
    courses = relationship("Course", back_populates="registrations")

