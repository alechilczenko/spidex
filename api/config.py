import os

class Config:
    DB_SERVER_NAME = os.environ.get("DB_SERVER_NAME")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

