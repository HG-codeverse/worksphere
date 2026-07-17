import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH"))

    DEBUG = os.getenv("DEBUG") == "True"
    WTF_CSRF_ENABLED = True 

    JWT_TOKEN_LOCATION = ["cookies"]

    JWT_COOKIE_SECURE = False

    JWT_COOKIE_CSRF_PROTECT = False