from fastapi import Depends, APIRouter
from src.database.session import get_session
from src.schema.course import CourseBase
from sqlalchemy.orm import Session
from src.services.course_service import get_courses, course_by_id, course_by_teacher_id, create_course

router = APIRouter(prefix="/course", tags=["course"])

@router.post("/")
def create_course_endpoint(course: CourseBase, db: Session = Depends(get_session)):
   
    return create_course(course, db)

@router.get("/")
def get_courses_endpoint(db: Session = Depends(get_session)):
    
    return get_courses(db)


@router.get("/{id}")
def course_by_id_endpoint(id: int, db: Session = Depends(get_session)):
    
    return course_by_id(id, db)


@router.get("/teacher/{teacher_id}")
def course_by_teacher_id_endpoint(teacher_id: int, db: Session = Depends(get_session)):
    
    return course_by_teacher_id(teacher_id, db)


