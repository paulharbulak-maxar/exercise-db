from sqlalchemy import URL
from sqlmodel import create_engine

from config import DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

if all([POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT]):
    url_object = URL.create(
        "postgresql",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=DB_HOST,
        database=POSTGRES_DB,
        port=DB_PORT,
    )
    print(url_object.render_as_string(hide_password=False))
    engine = create_engine(url_object)
else:
    sqlite_url = f"sqlite:///exercise.db"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
