from flask import request, jsonify
from marshmallow import ValidationError
from app.schemas.product_schema import ProductSchema
from app.services.product_service import create_product

def create_product_controller(data):
    try:
        data = ProductSchema().load(data)

        produto = create_product(data)

        return jsonify({
            "id": produto.id,
            "name": produto.name,
            "category": produto.category,
            "current_stock": produto.current_stock,
            "created_at": produto.created_at.isoformat(),
            "updated_at": produto.updated_at.isoformat()
        }), 201

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
