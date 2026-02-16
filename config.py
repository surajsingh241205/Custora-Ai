import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///custora.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

