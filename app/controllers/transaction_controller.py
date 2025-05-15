"""
Transaction controllers module.

Handles HTTP requests for creating entry and exit transactions, retrieving,
deleting, and filtering transactions, including JWT-based user identification.
"""

import os
from flask import request, jsonify, current_app, send_from_directory
from marshmallow import ValidationError
from app.schemas.transaction_schema import TransactionInputSchema
from app.services.transaction_service import (
    create_entry_transaction,
    create_exit_transaction,
    get_all_transactions_service,
    get_transactions_by_product,
    delete_transaction_by_id,
    get_transaction_by_id,
    get_transactions_by_user,
    get_ots_file_by_transaction_id
)
from app.utils.formatters import format_transaction
import jwt


def create_entry_controller():
    """
    Create an entry transaction for a product.

    Validates input data, decodes JWT to obtain user info,
    and delegates transaction creation to the service layer.

    Returns:
        Response: JSON-formatted transaction data with HTTP 201 on success,
                  or error messages with appropriate HTTP status.
    """
    try:
        # Validate and deserialize request JSON using TransactionInputSchema
        data = TransactionInputSchema().load(request.json)

        # Retrieve JWT from Authorization header and strip 'Bearer ' prefix
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            # Decode JWT to extract user ID and email
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            user_id = payload["user_id"]
            user_email = payload["email"]

        except jwt.ExpiredSignatureError:
            # JWT has expired
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            # JWT is invalid
            return jsonify({"error": "Invalid token"}), 401

        # Create entry transaction with user context
        transaction = create_entry_transaction(
            data,
            user_id=user_id,
            user_email=user_email
        )

        # Format and return transaction with 201 status
        return jsonify(format_transaction(transaction)), 201

    except ValidationError as ve:
        # Schema validation errors
        return jsonify({"errors": ve.messages}), 400

    except ValueError as ve:
        # Domain errors from service layer (e.g., invalid product)
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def create_exit_controller():
    """
    Create an exit transaction for a product.

    Validates input data, decodes JWT to obtain user info,
    and delegates transaction creation to the service layer.

    Returns:
        Response: JSON-formatted transaction data with HTTP 201 on success,
                  or error messages with appropriate HTTP status.
    """
    try:
        # Validate and deserialize request JSON using TransactionInputSchema
        data = TransactionInputSchema().load(request.json)

        # Retrieve JWT from Authorization header and strip 'Bearer ' prefix
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            # Decode JWT to extract user ID and email
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            user_id = payload["user_id"]
            user_email = payload["email"]
        except jwt.ExpiredSignatureError:
            # JWT has expired
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            # JWT is invalid
            return jsonify({"error": "Invalid token"}), 401

        # Create exit transaction with user context
        transaction = create_exit_transaction(
            data,
            user_email,
            user_id
        )

        # Format and return transaction with 201 status
        return jsonify(format_transaction(transaction)), 201

    except ValidationError as ve:
        # Schema validation errors
        return jsonify({"errors": ve.messages}), 400
    except ValueError as ve:
        # Domain errors from service layer (e.g., invalid product)
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def get_all_transactions_controller():
    """
    Retrieve all transactions.

    Returns:
        Response: JSON list of formatted transactions with HTTP 200,
                  or error message with HTTP 500.
    """
    try:
        # Fetch all transactions via service layer
        transactions = get_all_transactions_service()
        # Format and return list of transactions
        return jsonify([format_transaction(t) for t in transactions]), 200
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def get_transactions_by_product_controller(product_id):
    """
    Retrieve transactions filtered by product ID.

    Args:
        product_id (int): ID of the product to filter transactions.

    Returns:
        Response: JSON list of transactions with HTTP 200,
                  HTTP 404 if none found, or HTTP 500 on error.
    """
    try:
        transactions = get_transactions_by_product(product_id)

        if not transactions:
            # No transactions for the specified product
            return jsonify({"message": "No transactions found for this product"}), 404

        formatted = [format_transaction(t) for t in transactions]
        return jsonify(formatted), 200

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def delete_transaction_controller(id: int):
    """
    Delete a transaction by ID.

    Args:
        id (int): Identifier of the transaction to delete.

    Returns:
        Response: Success message with HTTP 200 if deleted,
                  or error message with HTTP 404.
    """
    # Attempt deletion via service layer
    success = delete_transaction_by_id(id)
    if success:
        return jsonify({"message": "Transaction deleted successfully"}), 200
    # Transaction not found in data store
    return jsonify({"error": "Transaction not found"}), 404


def get_transaction_by_id_controller(transaction_id):
    """
    Retrieve a single transaction by its ID.

    Args:
        transaction_id (int): Identifier of the transaction.

    Returns:
        Response: JSON-formatted transaction with HTTP 200,
                  HTTP 404 if not found, or HTTP 500 on error.
    """
    try:
        transaction = get_transaction_by_id(transaction_id)
        return jsonify(format_transaction(transaction)), 200
    except ValueError as ve:
        # Transaction not found or invalid ID
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500


def get_transactions_by_user_controller():
    """
    Retrieve transactions for the authenticated user.

    Extracts user ID from JWT and fetches their transactions.

    Returns:
        Response: JSON list of user's transactions with HTTP 200,
                  HTTP 404 if none found, or HTTP 401/500 on error.
    """
    try:
        # Retrieve JWT from Authorization header
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            # Decode JWT to extract user ID
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            # JWT has expired
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            # JWT is invalid
            return jsonify({"error": "Invalid token"}), 401

        # Fetch transactions for the authenticated user
        transactions = get_transactions_by_user(user_id)

        if not transactions:
            # No transactions for this user
            return jsonify({"message": "No transactions found for this user"}), 404

        formatted = [format_transaction(t) for t in transactions]
        return jsonify(formatted), 200

    except Exception as e:
        # Unexpected server error
        return jsonify({"error": str(e)}), 500

def verify_transaction_controller():
    from flask import request, jsonify
    from app.utils.ots_handler import verify_ots_file

    data = request.get_json()
    filename = data.get("ots_filename")

    if not filename:
        return jsonify({"error": "ots_filename is required"}), 400

    result = verify_ots_file(filename)

    if result.get("success"):
        return jsonify({
            "message": "Hash verified successfully",
            "details": result.get("output", "")
        }), 200
    else:
        return jsonify({
            "message": result.get("message", "Verification failed."),
            "details": result.get("output", "No additional info.")
        }), 400

def download_ots_controller(transaction_id: int):
    """
    Controller to return the .ots file for a given transaction ID.
    Handles response formatting and errors.

    Args:
        transaction_id (int): ID of the transaction.

    Returns:
        Response: OTS file or error JSON.
    """
    result = get_ots_file_by_transaction_id(transaction_id)

    if not result["success"]:
        return jsonify({"error": result["message"]}), 404

    return send_from_directory(
        directory=os.path.abspath(result["directory"]),
        path=result["filename"],
        as_attachment=True
    )
