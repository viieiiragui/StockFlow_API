import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from enum import Enum

def generate_jwt(user, expires_in=1):
    permission = user.permission.value if isinstance(user.permission, Enum) else user.permission

    payload = {
        "user_id": user.id,
        "email": user.email,
        "permission": permission,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        "iat": datetime.now(timezone.utc)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token
