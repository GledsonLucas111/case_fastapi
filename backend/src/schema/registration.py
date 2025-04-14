from pydantic import BaseModel

class RegistrationBase(BaseModel):
    student_id: int
    course_id: int