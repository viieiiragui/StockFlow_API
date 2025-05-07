"""
Configuration module.

Loads environment variables and defines application configuration parameters
such as database connection URI, secret key for JWT, and SQLAlchemy settings.
"""

import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://seu_user:suasenha@localhost/seu_banco")
    SECRET_KEY = os.getenv("SECRET_KEY", "123456789")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
