import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from app.infraBD.repositories.users_repository import UsersRepository
from flask import current_app

def authenticate_user(email: str, senha: str):
    repo = UsersRepository()
    user = repo.select_user_by_email(email=email)

    if not user or not bcrypt.checkpw(senha.encode(), user.password_hash.encode()):
        return None

    payload = {
        "user_id": user.id,
        "permission": user.permission.value,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token, user
