"""
User schema module.

Defines input validation schemas for user creation and update using Marshmallow.
Ensures required fields meet format and length constraints, and permissions match allowed values.
"""

from marshmallow import Schema, fields, validate


class UserInputSchema(Schema):
    """
    Schema for validating user creation payloads.

    Fields:
        name (str): Full name of the user; required.
        email (str): Valid email address; required.
        password (str): Password with minimum length of 6; required.
        permission (str): User permission level; must be one of 'admin', 'operator', or 'viewer'.
    """
    # Name field: required string
    name = fields.Str(
        required=True,
        error_messages={"required": "Name is required."}
    )
    # Email field: required and validated as email format
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required.",
                        "invalid": "Invalid email address format."}
    )
    # Password field: required string with at least 6 characters
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=6,
            error="Password must be at least 6 characters long."
        ),
        error_messages={"required": "Password is required."}
    )
    # Permission field: required string matching one of the allowed roles
    permission = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["admin", "operator", "viewer"],
            error="Permission must be 'admin', 'operator', or 'viewer'."
        ),
        error_messages={"required": "Permission is required."}
    )


class UserUpdateSchema(Schema):
    """
    Schema for validating user update payloads.

    All fields are optional; when provided, must meet the same constraints as creation schema.

    Fields:
        name (str, optional): New full name of the user.
        email (str, optional): Valid email address.
        password (str, optional): Password with minimum length of 6.
        permission (str, optional): User permission level; must be 'ADMIN' or 'VIEWER'.
    """
    # Name field: optional update
    name = fields.Str(
        required=False
    )
    # Email field: optional update, validated as email format
    email = fields.Email(
        required=False,
        error_messages={"invalid": "Invalid email address format."}
    )
    # Password field: optional update with at least 6 characters
    password = fields.Str(
        required=False,
        validate=validate.Length(
            min=6,
            error="Password must be at least 6 characters long."
        )
    )
    # Permission field: optional update, must be one of the allowed uppercase roles
    permission = fields.Str(
        required=False,
        validate=validate.OneOf(
            ["ADMIN", "VIEWER"],
            error="Permission must be 'ADMIN' or 'VIEWER'."
        )
    )
