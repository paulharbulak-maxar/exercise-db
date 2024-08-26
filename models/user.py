from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str
    last_name: str
    first_name: str
    email: str
    creation_date: datetime | None
    last_login_date: datetime | None
