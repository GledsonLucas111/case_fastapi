from fastapi import HTTPException
from src.models.user import User, Teacher, Student, Admin
from src.schema.user import (
    UserUpdate,
    StudentCreate,
    TeacherCreate,
    AdminCreate,
    Login,
)
from sqlalchemy.orm import Session


def get_users(db: Session):
    users = db.query(User).all()
    if len(users) == 0:
        raise HTTPException(status_code=404, detail="no users.")
    return users


def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def login(data: Login, db: Session):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="email or password incorrect.")

    if not user.password == data.password:
        raise HTTPException(status_code=401, detail="email or password incorrect.")

    return user


def create_user(user: StudentCreate | TeacherCreate | AdminCreate, db: Session):
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
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_user(id: int, user_update: UserUpdate, db: Session):
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


def delete_user(id: int, db: Session):
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
