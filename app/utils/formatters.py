from app.schemas.product_schema import ProductSchema

def format_product(product):
    return ProductSchema().dump(product)

def format_product_list(products):
    return ProductSchema(many=True).dump(products)
