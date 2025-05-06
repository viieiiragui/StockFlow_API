from flask import Blueprint
from app.controllers.transaction_controller import create_entry_controller, create_exit_controller, get_all_transactions_controller, get_transactions_by_product_controller, delete_transaction_controller, get_transaction_by_id_controller, get_transactions_by_user_controller
from app.auth.permissions import permission_required

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/entry", methods=["POST"])
@permission_required("operator")
def create_entry():
    return create_entry_controller()

@transaction_bp.route("/exit", methods=["POST"])
@permission_required("operator")
def create_exit():
    return create_exit_controller()

@transaction_bp.route("/transactions", methods=["GET"])
@permission_required("viewer")
def get_all_transactions():
    return get_all_transactions_controller()

@transaction_bp.route("/transactions/by-product/<int:product_id>", methods=["GET"])
@permission_required("viewer")
def get_transactions_by_product(product_id):
    return get_transactions_by_product_controller(product_id)

@transaction_bp.route("/transactions/<int:id>", methods=["DELETE"])
@permission_required("admin")
def delete_transaction(id):
    return delete_transaction_controller(id)

@transaction_bp.route("/transactions/<int:transaction_id>", methods=["GET"])
@permission_required("viewer")
def get_transaction_by_id_route(transaction_id):
    return get_transaction_by_id_controller(transaction_id)

@transaction_bp.route("/user/transactions", methods=["GET"])
@permission_required("viewer")
def get_transactions_by_user():
    return get_transactions_by_user_controller()
