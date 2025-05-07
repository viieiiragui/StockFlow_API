"""
Authentication blueprint module.

Defines the '/login' endpoint for user authentication,
delegating login logic to the user_login controller.
"""

from flask import Blueprint, request
from app.controllers.auth_controller import user_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle POST requests to '/login' for user authentication.

    Expects JSON payload with 'email' and 'password'.
    Delegates validation and token generation to user_login.

    Returns:
        Response: JSON response from user_login (access token and user info,
                  or error messages).
    """

    # Extract JSON body and delegate to the authentication controller
    return user_login(request.json)
