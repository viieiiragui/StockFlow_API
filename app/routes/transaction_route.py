from flask import Blueprint
from app.controllers.transaction_controller import create_entry_controller
from app.auth.permissions import permission_required

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/entry", methods=["POST"])
@permission_required("operator")
def create_entry():
    return create_entry_controller()
