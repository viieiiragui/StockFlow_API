"""
Product blueprint module.

Defines RESTful endpoints for product operations (CRUD) with JWT-based permission checks,
delegating business logic to controller functions.
"""

from flask import Blueprint, request
from app.controllers.product_controller import (
    create_product_controller,
    list_products_controller,
    get_product_controller,
    update_product_controller,
    delete_product_controller
)
from app.auth.permissions import permission_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/product', methods=['POST'])
@permission_required('admin')
def create_product():
    """
    Handle POST /product endpoint to create a new product.

    Requires 'admin' permission.
    Expects JSON payload with product attributes.

    Returns:
        Response: JSON-formatted created product and HTTP 201 on success,
                  or error message with appropriate status code.
    """
    return create_product_controller(request.json)

@product_bp.route('/product', methods=['GET'])
@permission_required('viewer')
def list_products():
    """
    Handle GET /product endpoint to list all products.

    Requires at least 'viewer' permission.
    Supports optional query parameters 'name' and 'code'.

    Returns:
        Response: JSON list of products and HTTP 200 on success,
                  or error message with HTTP 500 on failure.
    """
    return list_products_controller()

@product_bp.route('/product/<int:id>', methods=['GET'])
@permission_required('viewer')
def get_product(id):
    """
    Handle GET /product/<id> endpoint to retrieve a specific product.

    Requires at least 'viewer' permission.

    Args:
        id (int): Identifier of the product to fetch.

    Returns:
        Response: JSON-formatted product and HTTP 200 on success,
                  404 if not found, or error status on failure.
    """
    return get_product_controller(id)

@product_bp.route('/product/<int:id>', methods=['PUT'])
@permission_required('admin')
def update_product_route(id):
    """
    Handle PUT /product/<id> endpoint to update an existing product.

    Requires 'admin' permission.
    Expects JSON payload with fields to update (partial updates allowed).

    Args:
        id (int): Identifier of the product to update.

    Returns:
        Response: JSON-formatted updated product and HTTP 200 on success,
                  404 if not found, or error status on failure.
    """
    return update_product_controller(id)

@product_bp.route('/product/<int:id>', methods=['DELETE'])
@permission_required('admin')
def delete_product_route(id):
    """
    Handle DELETE /product/<id> endpoint to delete a product.

    Requires 'admin' permission.

    Args:
        id (int): Identifier of the product to delete.

    Returns:
        Response: JSON message and HTTP 200 on success,
                  or error message with HTTP 404 if not found.
    """
    return delete_product_controller(id)
