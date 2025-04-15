from fastapi import Depends, APIRouter
from src.database.session import get_session
from src.schema.registration import RegistrationBase
from sqlalchemy.orm import Session
from src.services.registration_service import create_registration, registratio_by_student_id
router = APIRouter(prefix="/registration", tags=["registration"])


@router.post("/")
def create_registration_endpoint(registration: RegistrationBase, db: Session = Depends(get_session)):
   
    return create_registration(registration, db)
   


@router.get("/student/{student_id}")
def registratio_by_student_id_endpoint(student_id: int, db: Session = Depends(get_session)):

    return registratio_by_student_id(student_id, db)
