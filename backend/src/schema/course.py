from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    video: str
    teacher_id: int
    
    