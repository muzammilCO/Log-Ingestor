import os
import json
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv


class Settings:
    load_dotenv(find_dotenv(filename=".env.dev"))
    print("Here")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
    DATABASE_PORT: int = os.environ.get("DATABASE_PORT")
    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE_URL: str = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


@lru_cache
def get_app_settings():
    return Settings()
