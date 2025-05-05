from app.infraBD.models.products import Products
from app.infraBD.config.connection import db
from datetime import datetime, timezone

class ProductsRepository:
    def insert_product(self, data: dict):
        data_insert = Products(
            name=data["name"],
            category=data["category"],
            current_stock=data["current_stock"]
        )

        db.session.add(data_insert)
        db.session.commit()

        return data_insert

    def update_product(self, id: int, name: str = None, category: str = None, current_stock: int = None, add_stock: int = None):
        actual_product = db.session.query(Products).filter(Products.id==id).first()
        
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
        result = db.session.query(Products).filter(Products.id==id).delete()
        db.session.commit()

        return result > 0

    def select_all_products(self):
        data = db.session.query(Products).all()
        return data
    
    def select_by_name(self, name):
        return db.session.query(Products).filter(Products.name.ilike(name)).first()
