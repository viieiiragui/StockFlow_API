from flask import Blueprint, request
from app.controllers.product_controller import create_product_controller
from app.auth.permissions import permission_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/product', methods=['POST'])
@permission_required('admin')
def create():
    return create_product_controller(request.json)
