import urllib
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlmodel import create_engine

load_dotenv()
# TODO: Move to config.py
POSTGRES_DB = environ.get("POSTGRES_DB", "exercise")
POSTGRES_USER = environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = int(environ.get("DB_PORT", 4321))

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
    backend_root = Path(__file__).resolve().parents[4]
    sqlite_db = backend_root / "exercise.db"
    sqlite_url = f"sqlite:///{sqlite_db.as_posix()}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
