"""
Login schema module.

Defines the input validation schema for user login requests using Marshmallow.
Validates required email and password fields.
"""

from marshmallow import Schema, fields


class LoginSchema(Schema):
    """
    Schema for validating login payloads.

    Fields:
        email (str): User email address; must be a valid email format.
        password (str): User password; must be a non-empty string.
    """
    
    # Email field: required and must be a valid email address
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required.",
                        "invalid": "Invalid email address format."}
    )
    # Password field: required string
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required.",
                        "null": "Password cannot be null."}
    )