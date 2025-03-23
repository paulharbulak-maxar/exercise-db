from os import environ

from dotenv import load_dotenv

load_dotenv()
# TODO: Move to config.py
POSTGRES_DB = environ["POSTGRES_DB"]
POSTGRES_USER = environ["POSTGRES_USER"]
POSTGRES_PASSWORD = environ["POSTGRES_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_PORT = int(environ["DB_PORT"])
