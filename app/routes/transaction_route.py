"""
Transaction blueprint module.

Defines endpoints for creating entry and exit transactions, retrieving, and deleting transactions
with JWT-based permission checks, delegating logic to controller functions.
"""

from flask import Blueprint
from app.controllers.transaction_controller import (
    create_entry_controller,
    create_exit_controller,
    get_all_transactions_controller,
    get_transactions_by_product_controller,
    delete_transaction_controller,
    get_transaction_by_id_controller,
    get_transactions_by_user_controller,
    verify_transaction_controller
)
from app.auth.permissions import permission_required

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/api/transactions/entry', methods=['POST'])  # Endpoint to create entry transactions
@permission_required('operator')
def create_entry():
    """
    Handle POST /api/transactions/entry to create an entry transaction for a product.

    Requires 'operator' permission.
    Delegates to create_entry_controller which validates input and decodes JWT.

    Returns:
        Response: JSON-formatted transaction and HTTP 201 on success,
                  or error messages with appropriate status codes.
    """
    return create_entry_controller()

@transaction_bp.route('/api/transactions/exit', methods=['POST'])  # Endpoint to create exit transactions
@permission_required('operator')
def create_exit():
    """
    Handle POST /api/transactions/exit to create an exit transaction for a product.

    Requires 'operator' permission.
    Delegates to create_exit_controller which validates input and decodes JWT.

    Returns:
        Response: JSON-formatted transaction and HTTP 201 on success,
                  or error messages with appropriate status codes.
    """
    return create_exit_controller()

@transaction_bp.route('/api/transactions', methods=['GET'])  # Endpoint to list all transactions
@permission_required('viewer')
def get_all_transactions():
    """
    Handle GET /api/transactions to retrieve all transactions.

    Requires 'viewer' permission.

    Returns:
        Response: JSON list of transactions and HTTP 200 on success,
                  or error message with HTTP 500 on failure.
    """
    return get_all_transactions_controller()

@transaction_bp.route('/api/transactions/by-product/<int:product_id>', methods=['GET'])  # Filter transactions by product
@permission_required('viewer')
def get_transactions_by_product(product_id):
    """
    Handle GET /api/transactions/by-product/<product_id> to retrieve transactions for a specific product.

    Requires 'viewer' permission.

    Args:
        product_id (int): ID of the product to filter transactions.

    Returns:
        Response: JSON list of transactions and HTTP 200 on success,
                  or 404/500 on error.
    """
    return get_transactions_by_product_controller(product_id)

@transaction_bp.route('/api/transactions/delete/<int:id>', methods=['DELETE'])  # Endpoint to delete a transaction
@permission_required('admin')
def delete_transaction(id):
    """
    Handle DELETE /api/transactions/<id> to remove a transaction by its ID.

    Requires 'admin' permission.

    Args:
        id (int): Identifier of the transaction to delete.

    Returns:
        Response: Success message and HTTP 200 on success,
                  or error message with HTTP 404 if not found.
    """
    return delete_transaction_controller(id)

@transaction_bp.route('/api/transactions/<int:transaction_id>', methods=['GET'])  # Endpoint to get a transaction by ID
@permission_required('viewer')
def get_transaction_by_id_route(transaction_id):
    """
    Handle GET /api/transactions/<transaction_id> to retrieve a specific transaction by its ID.

    Requires 'viewer' permission.

    Args:
        transaction_id (int): Identifier of the transaction.

    Returns:
        Response: JSON-formatted transaction and HTTP 200 on success,
                  or error message with HTTP 404/500 on failure.
    """
    return get_transaction_by_id_controller(transaction_id)

@transaction_bp.route('/api/user/transactions', methods=['GET'])  # Endpoint to get transactions for authenticated user
@permission_required('viewer')
def get_transactions_by_user():
    """
    Handle GET /api/user/transactions to retrieve transactions of the authenticated user.

    Requires 'viewer' permission.
    Delegates JWT decoding and retrieval to controller.

    Returns:
        Response: JSON list of user transactions and HTTP 200 on success,
                  or error message with HTTP 401/404/500 on failure.
    """
    return get_transactions_by_user_controller()

@transaction_bp.route('/api/transactions/verify', methods=['POST'])
@permission_required('viewer')
def verify_transaction():
    """
    Handle POST /api/transactions/verify to validate the integrity of a transaction
    by checking its OTS file.

    Requires 'viewer' permission.

    Request JSON:
        {
            "ots_filename": "transacao_4_4_entry_admin_at_email_com_20250515T183422.bin.ots"
        }

    Returns:
        Response: JSON with verification result and blockchain anchoring details.
    """
    return verify_transaction_controller()
