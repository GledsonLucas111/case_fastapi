from fastapi import FastAPI, Depends, HTTPException, status
from src.database.session import get_session
from src.models.user import User, Teacher, Student, Admin, Course, Registration
from src.schema.user import (
    UserUpdate,
    StudentCreate,
    TeacherCreate,
    AdminCreate,
    UserBase,
    CourseBase,
    RegistrationBase,
    Login,
)
from sqlalchemy.orm import Session
from src.database.session import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/")
def get_users(db: Session = Depends(get_session)):
    users = db.query(User).all()
    user_response = []
    for user in users:
        user_response.append(
            {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
        )
    return user_response


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


@app.post("/login/")
async def login(data: Login, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="email or password incorrect.")

    if not user.password == data.password:
        raise HTTPException(status_code=401, detail="email or password incorrect.")

    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


@app.post("/users/")
def create_user(
    user: StudentCreate | TeacherCreate | AdminCreate,
    db: Session = Depends(get_session),
):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exist.")

    if user.role == "teacher":
        if (
            not hasattr(user, "specialization")
            or not user.specialization
            or not user.specialization.strip()
        ):
            raise HTTPException(
                status_code=400, detail="Specialization needed for teachers"
            )

    if user.role == "student":
        if (
            not hasattr(user, "registration")
            or not user.registration
            or not user.registration.strip()
        ):
            raise HTTPException(
                status_code=400, detail="Registration needed for student"
            )

    if isinstance(user, StudentCreate):
        new_user = Student(
            name=user.name,
            email=user.email,
            password=user.password,
            registration=user.registration,
        )
    elif isinstance(user, TeacherCreate):
        new_user = Teacher(
            name=user.name,
            email=user.email,
            password=user.password,
            specialization=user.specialization,
        )
    else:
        new_user = Admin(name=user.name, email=user.email, password=user.password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id": new_user.id, "nome": new_user.name, "role": new_user.role}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/users/{id}")
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.role != user_update.role:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de atualização incompatível com o usuário (esperado: {user.role})",
        )

    update_data = user_update.model_dump(exclude_unset=True, exclude={"role"})
    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    try:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/course")
def courses(db: Session = Depends(get_session)):
    course = db.query(Course).all()

    if not course:
        raise HTTPException(status_code=404, detail="Courses not found.")

    return course

@app.get("/course/{id}")
def course_by_id(id: int, db: Session = Depends(get_session)):
    course = db.query(Course).filter(Course.id == id).all()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    return course


@app.get("/courses/{teacher_id}")
def course_by_teacher_id(teacher_id: int, db: Session = Depends(get_session)):
    course = db.query(Course).filter(Course.teacher_id == teacher_id).all()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    return course


@app.post("/course")
def create_course(course: CourseBase, db: Session = Depends(get_session)):
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
        return {"message": "course created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/registration")
def create_registration(
    registration: RegistrationBase, db: Session = Depends(get_session)
):
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
        return {"message": "registration created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/registration/{student_id}")
def registratio_by_student_id(student_id: int, db: Session = Depends(get_session)):
    registration = db.query(Registration).filter(student_id == Registration.student_id).all()
    
    if not registration:
        raise HTTPException(status_code=404, detail="registration not found.")
    

    return registration
