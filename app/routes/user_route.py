"""
User blueprint module.

Defines RESTful endpoints for user management (CRUD), all protected by 'admin' permission,
delegating request handling to the corresponding controller functions.
"""

from flask import Blueprint
from app.controllers.user_controller import (
    create_user_controller,
    get_all_users_controller,
    get_user_by_id_controller,
    update_user_controller,
    delete_user_controller
)
from app.auth.permissions import permission_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["POST"])
@permission_required("admin")
def create_user():
    """
    Handle POST /users to create a new user.

    Requires 'admin' permission.
    Delegates to create_user_controller, which validates input via UserInputSchema
    and creates the user in the database.

    Returns:
        Response: JSON-formatted created user and HTTP 201 on success,
                  or error messages with HTTP 400/409/500 on failure.
    """
    return create_user_controller()

@user_bp.route("/users", methods=["GET"])
@permission_required("admin")
def list_users():
    """
    Handle GET /users to retrieve all users.

    Requires 'admin' permission.
    Delegates to get_all_users_controller, which fetches and formats user list.

    Returns:
        Response: JSON list of users and HTTP 200 on success,
                  or error message with HTTP 500 on failure.
    """
    return get_all_users_controller()

@user_bp.route("/users/<int:id>", methods=["GET"])
@permission_required("admin")
def get_user_by_id(id):
    """
    Handle GET /users/<id> to retrieve a single user by ID.

    Requires 'admin' permission.

    Args:
        id (int): Identifier of the user to fetch; must be positive.

    Returns:
        Response: JSON-formatted user and HTTP 200 if found,
                  or error messages with HTTP 400/404 on invalid or missing user.
    """
    return get_user_by_id_controller(id)

@user_bp.route("/users/<int:id>", methods=["PUT"])
@permission_required("admin")
def update_user(id):
    """
    Handle PUT /users/<id> to update an existing user.

    Requires 'admin' permission.
    Delegates to update_user_controller, which validates input via UserUpdateSchema
    and applies changes.

    Args:
        id (int): Identifier of the user to update; must be positive.

    Returns:
        Response: JSON-formatted updated user and HTTP 200 on success,
                  or error messages with HTTP 400/404/500 on failure.
    """
    return update_user_controller(id)

@user_bp.route("/users/<int:id>", methods=["DELETE"])
@permission_required("admin")
def delete_user(id):
    """
    Handle DELETE /users/<id> to remove a user by ID.

    Requires 'admin' permission.

    Args:
        id (int): Identifier of the user to delete; must be positive.

    Returns:
        Response: JSON message and HTTP 200 on success,
                  or error message with HTTP 404 if not found.
    """
    return delete_user_controller(id)
