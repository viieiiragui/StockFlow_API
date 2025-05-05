from functools import wraps
from flask import request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import current_app

def permission_required(required_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')

            if not token:
                return jsonify({"error": "Token not provided"}), 401

            try:
                payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                permission = payload.get("permission")

                if permission is None:
                    return jsonify({"error": "Permission not found in token"}), 401

                # Permission hierarchy
                levels = {
                    "viewer": 1,
                    "operator": 2,
                    "admin": 3
                }

                if levels.get(permission, 0) < levels.get(required_level, 0):
                    return jsonify({"error": "Insufficient permission"}), 403

                return func(*args, **kwargs)

            except ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401

            except InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

        return wrapper
    return decorator
