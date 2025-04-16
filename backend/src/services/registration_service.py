from fastapi import  HTTPException
from src.models.user import Student
from src.models.course import Course
from src.models.registration import Registration
from src.schema.registration import RegistrationBase
from sqlalchemy.orm import Session


def create_registration(registration: RegistrationBase, db: Session):
    if not db.query(Student).filter(Student.id == registration.student_id).first():
        raise HTTPException(
            status_code=400, detail="the Student with this ID is not registered."
        )
    if not db.query(Course).filter(Course.id == registration.course_id).first():
        raise HTTPException(
            status_code=400, detail="the course with this ID is not registered."
        )

    new_registration = Registration(
        student_id=registration.student_id, course_id=registration.course_id
    )

    try:
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        return new_registration
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def registratio_by_student_id(student_id: int, db: Session):
    registration = (
        db.query(Registration).filter(student_id == Registration.student_id).all()
    )

    if not registration:
        raise HTTPException(status_code=404, detail="registration not found.")

    return registration
