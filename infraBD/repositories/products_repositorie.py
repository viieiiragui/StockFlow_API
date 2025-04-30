from infraBD.models.products import Product
from infraBD.config.connection import db
from datetime import datetime, timezone

class ProductsRepository:
    def insert_product(self, name: str, category: str, current_stock: int):
        data_insert = Product(
            name = name,
            category = category,
            current_stock = current_stock,
        )

        db.session.add(data_insert)
        db.session.commit()

        return data_insert

    def update_product(self, id: int, name: str = None, category: str = None, current_stock: int = None, add_stock: int = None):
        actual_product = db.session.query(Product).filter(Product.id==id).first()
        
        if not actual_product:
            return None

        if current_stock is not None and add_stock is not None:
            raise ValueError("Use 'current_stock' or 'add_stock'")

        if name is not None:
            actual_product.name = name
        if category is not None:
            actual_product.category = category
        if current_stock is not None:
            actual_product.current_stock = current_stock
        if add_stock is not None:
            actual_product.current_stock += add_stock
        
        actual_product.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return actual_product

    def delete_product(self, id: int):
        result = db.session.query(Product).filter(Product.id==id).delete()
        db.session.commit()

        return result > 0

    def select_all_products(self):
        data = db.session.query(Product).all()
        return data
    