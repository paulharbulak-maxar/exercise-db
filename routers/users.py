from fastapi import APIRouter
from sqlmodel import Session, select

from models.user import User
from routers.utils.database import engine

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/", response_model=list[User])
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
