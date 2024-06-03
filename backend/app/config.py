import os
import urllib.parse
# from flask import Flask

# app = Flask(__name__)

POSTGRES_USER = os.getenv("POSTGRES_USER", "username")
POSTGRES_PASSWORD = urllib.parse.quote(os.getenv("POSTGRES_PASSWORD", "password"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key') # configure when adding user auth