from flask import jsonify
from marshmallow import ValidationError
from app.schemas.login_schema import LoginSchema
from app.services.auth_service import authenticate_user

def user_login(data):
    try:
        valid_data = LoginSchema().load(data)

        result = authenticate_user(valid_data["email"], valid_data["password"])
        if result is None:
            return jsonify({"error": "Invalid credentials"}), 401

        token, user = result

        return jsonify({
            "access_token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "permission": user.permission.value
            }
        }), 200

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
