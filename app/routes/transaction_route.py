from flask import Blueprint
from app.controllers.transaction_controller import create_entry_controller, create_exit_controller, get_all_transactions_controller
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
