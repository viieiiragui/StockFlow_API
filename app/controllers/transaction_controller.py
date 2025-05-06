from flask import request, jsonify, current_app
from marshmallow import ValidationError
from app.schemas.transaction_schema import TransactionInputSchema
from app.services.transaction_service import create_entry_transaction, create_exit_transaction, get_all_transactions_service, get_transactions_by_product, delete_transaction_by_id, get_transaction_by_id, get_transactions_by_user
from app.utils.formatters import format_transaction
import jwt

def create_entry_controller():
    try:
        data = TransactionInputSchema().load(request.json)

        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["user_id"]
            user_email = payload["email"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        transaction = create_entry_transaction(data, user_id=user_id, user_email=user_email)

        return jsonify(format_transaction(transaction)), 201

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_exit_controller():
    try:
        data = TransactionInputSchema().load(request.json)

        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["user_id"]
            user_email = payload["email"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        transaction = create_exit_transaction(data, user_email, user_id)

        return jsonify(format_transaction(transaction)), 201

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_transactions_controller():
    try:
        transactions = get_all_transactions_service()
        return jsonify([format_transaction(t) for t in transactions]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_transactions_by_product_controller(product_id):
    try:
        transactions = get_transactions_by_product(product_id)

        if not transactions:
            return jsonify({"message": "No transactions found for this product"}), 404

        formatted = [format_transaction(t) for t in transactions]
        return jsonify(formatted), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_transaction_controller(id: int):
    success = delete_transaction_by_id(id)
    if success:
        return jsonify({"message": "Transaction deleted successfully"}), 200
    return jsonify({"error": "Transaction not found"}), 404

def get_transaction_by_id_controller(transaction_id):
    try:
        transaction = get_transaction_by_id(transaction_id)
        return jsonify(format_transaction(transaction)), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_transactions_by_user_controller():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        transactions = get_transactions_by_user(user_id)

        if not transactions:
            return jsonify({"message": "No transactions found for this user"}), 404

        formatted = [format_transaction(t) for t in transactions]
        return jsonify(formatted), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
