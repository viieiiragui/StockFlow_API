from flask import request, jsonify
from marshmallow import ValidationError
from app.schemas.product_schema import ProductSchema
from app.utils.formatters import format_product, format_product_list
from app.services.product_service import create_product, get_product_by_id, get_all_products, update_product, delete_product

def create_product_controller(data):
    try:
        data = ProductSchema().load(data)

        produto = create_product(data)

        return jsonify(format_product(produto)), 201

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def list_products_controller():
    try:
        name = request.args.get("name")

        products = get_all_products(name)

        return jsonify(format_product_list(products)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_product_controller(id):
    try:
        product = get_product_by_id(id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(format_product(product)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_product_controller(id):
    try:
        schema = ProductSchema(partial=True)
        data = schema.load(request.json)

        product = update_product(id, data)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(format_product(product)), 200

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_product_controller(id):
    try:
        delete_product(id)
        return jsonify({"message": f"Product {id} successfully deleted."}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
