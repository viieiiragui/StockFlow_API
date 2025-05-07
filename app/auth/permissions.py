"""
Permission decorator module.

Provides a decorator to enforce JWT-based permission levels on Flask endpoints.
"""

from functools import wraps
from flask import request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import current_app

def permission_required(required_level):
    """
    Decorator factory that creates a decorator to check for required permission level.

    Args:
        required_level (str): The minimum permission level required (e.g., 'viewer', 'operator', 'admin').

    Returns:
        function: A decorator that enforces the permission check.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that validates JWT and checks the user's permission.

            Args:
                *args: Positional arguments forwarded to the decorated function.
                **kwargs: Keyword arguments forwarded to the decorated function.

            Returns:
                Response: Original function response if authorized, or JSON error with appropriate HTTP status.
            """
            # Retrieve the token from the Authorization header, stripping 'Bearer ' prefix if present
            token = request.headers.get('Authorization', '').replace('Bearer ', '')

            # If no token is provided, return unauthorized error
            if not token:
                return jsonify({"error": "Token not provided"}), 401

            try:
                # Decode the JWT using the application's secret key
                payload = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=["HS256"]
                )
                permission = payload.get("permission")

                # Ensure the permission field is present in the token payload
                if permission is None:
                    return jsonify({"error": "Permission not found in token"}), 401

                # Define permission hierarchy mapping
                levels = {
                    "viewer": 1,
                    "operator": 2,
                    "admin": 3
                }

                # Check if the user's permission level meets the required level
                if levels.get(permission, 0) < levels.get(required_level, 0):
                    return jsonify({"error": "Insufficient permission"}), 403

                # Permission is sufficient; proceed to the decorated function
                return func(*args, **kwargs)

            except ExpiredSignatureError:
                # Token has expired; return unauthorized error
                return jsonify({"error": "Token expired"}), 401

            except InvalidTokenError:
                # Token is invalid; return unauthorized error
                return jsonify({"error": "Invalid token"}), 401

        return wrapper
    return decorator
