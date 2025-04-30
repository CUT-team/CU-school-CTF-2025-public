import os

class Config:
    TOKEN = os.environ.get("TOKEN")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST", "db")
    DB_PORT = int(os.environ.get("DB_PORT", 5432))
    ADMIN_ID = int(os.environ.get("ADMIN_ID", 846318398))