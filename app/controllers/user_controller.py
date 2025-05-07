"""
User controllers module.

Defines CRUD controller functions for user resources, handling HTTP requests,
validating input, invoking service layer operations, and formatting responses.
"""

from flask import request, jsonify
from app.schemas.user_schema import UserInputSchema, UserUpdateSchema
from app.services.user_service import (
    create_user_service,
    get_all_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service
)
from app.utils.formatters import format_user
from marshmallow import ValidationError


def create_user_controller():
    """
    Handle HTTP request to create a new user.

    Validates input data against UserInputSchema and delegates creation
    to the service layer.

    Returns:
        Response: JSON-formatted created user with HTTP 201 on success,
                  or error messages with HTTP 400/409/500 on failure.
    """
    try:
        # Validate and deserialize request JSON using UserInputSchema
        data = UserInputSchema().load(request.json)

        # Create user via service layer
        user = create_user_service(data)

        # Format and return created user with 201 status
        return jsonify(format_user(user)), 201

    except ValidationError as ve:
        # Input validation errors: return details with 400 status
        return jsonify({"errors": ve.messages}), 400

    except ValueError as ve:
        # Conflict errors from service layer (e.g., duplicate email)
        return jsonify({"error": str(ve)}), 409

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def get_all_users_controller():
    """
    Handle HTTP request to retrieve all users.

    Returns:
        Response: JSON list of formatted users with HTTP 200 on success,
                  or error message with HTTP 500 on failure.
    """
    try:
        # Fetch all users via service layer
        users = get_all_users_service()

        # Format and return list of users
        return jsonify([format_user(user) for user in users]), 200

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def get_user_by_id_controller(id: int):
    """
    Handle HTTP request to retrieve a single user by ID.

    Args:
        id (int): Identifier of the user to retrieve; must be positive.

    Returns:
        Response: JSON-formatted user with HTTP 200 if found,
                  400 for invalid ID, 404 if not found, or 500 on error.
    """
    try:
        # Validate that ID is a positive integer
        if id <= 0:
            return jsonify({"error": "User ID must be a positive integer"}), 400

        # Fetch user by ID via service layer
        user = get_user_by_id_service(id)

        # Format and return the found user with 200 status
        return jsonify(format_user(user)), 200

    except ValueError as ve:
        # Service layer error when user not found
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def update_user_controller(id):
    """
    Handle HTTP request to update an existing user.

    Args:
        id (int): Identifier of the user to update; must be positive.

    Returns:
        Response: JSON-formatted updated user with HTTP 200 on success,
                  or error messages with HTTP 400/404/500 on failure.
    """
    try:
        # Validate that ID is positive
        if id <= 0:
            return jsonify({"error": "User ID must be positive"}), 400

        # Validate and deserialize request JSON using UserUpdateSchema
        data = UserUpdateSchema().load(request.json)

        # Update user via service layer
        updated = update_user_service(id, data)

        # Format and return updated user with 200 status
        return jsonify(format_user(updated)), 200

    except ValidationError as ve:
        # Input validation errors: return details with 400 status
        return jsonify({"errors": ve.messages}), 400
    except ValueError as ve:
        # Service layer error when user not found
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def delete_user_controller(id):
    """
    Handle HTTP request to delete a user by ID.

    Args:
        id (int): Identifier of the user to delete; must be positive.

    Returns:
        Response: Success message with HTTP 200 on deletion,
                  or error messages with HTTP 400/404/500 on failure.
    """
    try:
        # Validate that ID is positive
        if id <= 0:
            return jsonify({"error": "User ID must be positive"}), 400

        # Delete user via service layer
        delete_user_service(id)

        # Return success message with 200 status
        return jsonify({"message": "User deleted successfully"}), 200

    except ValueError as ve:
        # Service layer error when user not found
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500
