import os
import urllib.parse
from datetime import timedelta

POSTGRES_USER = os.getenv("POSTGRES_USER", "username")
POSTGRES_PASSWORD = urllib.parse.quote(os.getenv("POSTGRES_PASSWORD", "password"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = JWT_SECRET
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
