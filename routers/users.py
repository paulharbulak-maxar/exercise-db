from fastapi import APIRouter
from sqlmodel import Session, select

from models.models import User
from models.schemas import UserCreate, UserRead
from shared.utils.database import engine

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=UserRead)
def create_user(user: UserCreate):
    db_user = User(**user.model_dump())

    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.get("", response_model=list[UserRead])
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
