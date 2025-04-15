from fastapi import Depends, APIRouter
from src.database.session import get_session
from src.schema.user import (
    UserUpdate,
    StudentCreate,
    TeacherCreate,
    AdminCreate,
    Login,
    UserResponse,
)
from sqlalchemy.orm import Session
from src.services.user_service import (
    get_users,
    get_user,
    login,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_users_endpoint(db: Session = Depends(get_session)):

    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_session)):

    return get_user(user_id, db)


@router.post("/login", response_model=UserResponse)
async def login_endpoint(data: Login, db: Session = Depends(get_session)):

    return login(data, db)


@router.post("/", response_model=UserResponse)
def create_user_endpoint(
    user: StudentCreate | TeacherCreate | AdminCreate,
    db: Session = Depends(get_session),
):

    return create_user(user, db)


@router.patch("/{id}")
def update_user_endpoint(
    id: int, user_update: UserUpdate, db: Session = Depends(get_session)
):

    return update_user(id, user_update, db)


@router.delete("/{id}")
def delete_user_endpoint(id: int, db: Session = Depends(get_session)):

    return delete_user(id, db)
