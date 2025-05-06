from flask import request, jsonify, current_app
from marshmallow import ValidationError
from app.schemas.transaction_schema import TransactionInputSchema
from app.services.transaction_service import create_entry_transaction, create_exit_transaction, get_all_transactions_service
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
