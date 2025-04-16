from fastapi import Depends, HTTPException
from src.database.session import get_session
from src.models.user import Teacher
from src.models.course import Course
from src.schema.course import CourseBase
from sqlalchemy.orm import Session


def get_courses(db: Session):
    course = db.query(Course).all()

    if not course:
        raise HTTPException(status_code=404, detail="Courses not found.")

    return course


def course_by_id(id: int, db: Session):
    course = db.query(Course).filter(Course.id == id).all()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    return course


def course_by_teacher_id(teacher_id: int, db: Session):
    course = db.query(Course).filter(Course.teacher_id == teacher_id).all()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    return course


def create_course(course: CourseBase, db: Session):
    teacher = db.query(Teacher).filter(Teacher.id == course.teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=400, detail="the teacher with this ID is not registered."
        )

    new_course = Course(
        name=course.name, video=course.video, teacher_id=course.teacher_id
    )

    try:
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
