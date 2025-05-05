import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://seu_user:suasenha@localhost/seu_banco")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
