from flask import request, jsonify
from app.schemas.user_schema import UserInputSchema, UserUpdateSchema
from app.services.user_service import create_user_service, get_all_users_service, get_user_by_id_service, update_user_service, delete_user_service
from app.utils.formatters import format_user
from marshmallow import ValidationError

def create_user_controller():
    try:
        data = UserInputSchema().load(request.json)
        user = create_user_service(data)
        return jsonify(format_user(user)), 201
    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_users_controller():
    try:
        users = get_all_users_service()
        return jsonify([format_user(user) for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_by_id_controller(id: int):
    try:
        if id <= 0:
            return jsonify({"error": "User ID must be a positive integer"}), 400

        user = get_user_by_id_service(id)
        return jsonify(format_user(user)), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_user_controller(id):
    try:
        if id <= 0:
            return jsonify({"error": "User ID must be positive"}), 400

        data = UserUpdateSchema().load(request.json)
        updated = update_user_service(id, data)

        return jsonify(format_user(updated)), 200

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user_controller(id):
    try:
        if id <= 0:
            return jsonify({"error": "User ID must be positive"}), 400

        delete_user_service(id)
        return jsonify({"message": "User deleted successfully"}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
