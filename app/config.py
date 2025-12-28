from datetime import timedelta
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)     # e.g., 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)     # e.g., 7 days

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max upload