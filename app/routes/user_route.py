from flask import Blueprint
from app.controllers.user_controller import create_user_controller, get_all_users_controller, get_user_by_id_controller, update_user_controller, delete_user_controller
from app.auth.permissions import permission_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["POST"])
@permission_required("admin")
def create_user():
    return create_user_controller()

@user_bp.route("/users", methods=["GET"])
@permission_required("admin")
def list_users():
    return get_all_users_controller()

@user_bp.route("/users/<int:id>", methods=["GET"])
@permission_required("admin")
def get_user_by_id(id):
    return get_user_by_id_controller(id)

@user_bp.route("/users/<int:id>", methods=["PUT"])
@permission_required("admin")
def update_user(id):
    return update_user_controller(id)

@user_bp.route("/users/<int:id>", methods=["DELETE"])
@permission_required("admin")
def delete_user(id):
    return delete_user_controller(id)
