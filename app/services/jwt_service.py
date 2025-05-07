"""
JWT service module.

Handles generation of JSON Web Tokens for authenticated users, embedding
user identity and permission claims with expiration and issuance timestamps.
"""

import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from enum import Enum


def generate_jwt(user, expires_in=1):
    """
    Generate a JWT for a given user.

    Args:
        user: User object containing 'id', 'email', and 'permission' attributes.
        expires_in (int, optional): Token lifetime in hours (default is 1 hour).

    Returns:
        str: Encoded JWT as a string.
    """
    # Determine permission value; supports Enum or raw string
    permission = (
        user.permission.value
        if isinstance(user.permission, Enum)
        else user.permission
    )

    # Build token payload with standard and custom claims
    payload = {
        "user_id": user.id,
        "email": user.email,
        "permission": permission,
        # Expiration time: current UTC time plus expires_in hours
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        # Issued-at timestamp
        "iat": datetime.now(timezone.utc)
    }

    # Encode payload into JWT string using secret key and HS256 algorithm
    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return token
