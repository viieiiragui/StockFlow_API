"""
Login handler module.

Defines the user_login function to validate credentials, authenticate a user, and return a JWT and user info.
"""

from flask import jsonify
from marshmallow import ValidationError
from app.schemas.login_schema import LoginSchema
from app.services.auth_service import authenticate_user

def user_login(data):
    """
    Handle user login by validating input data and generating an access token.

    Args:
        data (dict): The JSON payload containing 'email' and 'password'.

    Returns:
        Response: A Flask JSON response with either:
                  - 200 and {'access_token': token, 'user': {...}} on success.
                  - 401 with an error message for invalid credentials.
                  - 400 with validation error details.
                  - 500 with a generic error message for unexpected exceptions.
    """
    try:
        # Validate incoming data against the LoginSchema
        valid_data = LoginSchema().load(data)

        # Attempt to authenticate user with validated credentials
        result = authenticate_user(valid_data["email"], valid_data["password"])
        if result is None:
            # Authentication failed: invalid email or password
            return jsonify({"error": "Invalid credentials"}), 401

        # Unpack returned token and user object
        token, user = result

        # Build and return success response with token and user details
        return jsonify({
            "access_token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "permission": user.permission.value
            }
        }), 200

    except ValidationError as ve:
        # Input data did not pass schema validation
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": str(e)}), 500
