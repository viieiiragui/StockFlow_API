from flask import Blueprint, request
from app.controllers.product_controller import create_product_controller, list_products_controller, get_product_controller, update_product_controller, delete_product_controller
from app.auth.permissions import permission_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/product', methods=['POST'])
@permission_required('admin')
def create():
    return create_product_controller(request.json)

@product_bp.route("/product", methods=["GET"])
@permission_required("viewer")
def list_products():
    return list_products_controller()

@product_bp.route("/product/<int:id>", methods=["GET"])
@permission_required("viewer")
def get_product(id):
    return get_product_controller(id)

@product_bp.route("/product/<int:id>", methods=["PUT"])
@permission_required("admin")
def update_product_route(id):
    return update_product_controller(id)

@product_bp.route("/product/<int:id>", methods=["DELETE"])
@permission_required("admin")
def delete_product_route(id):
    return delete_product_controller(id)
