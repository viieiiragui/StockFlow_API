from app.infraDB.models.products import Products
from app.infraDB.config.connection import db
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
        product = db.session.query(Products).filter(Products.id == id).first()

        if not product:
            return None

        if current_stock is not None and add_stock is not None:
            raise ValueError("Use only current_stock OR add_stock")

        if name is not None:
            product.name = name
        if category is not None:
            product.category = category
        if current_stock is not None:
            product.current_stock = current_stock
        if add_stock is not None:
            product.current_stock += add_stock

        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return product

    def delete_product(self, id: int):
        result = db.session.query(Products).filter(Products.id==id).delete()
        db.session.commit()

        return result > 0

    def select_all_products(self):
        data = db.session.query(Products).all()
        return data
    
    def select_by_name(self, name):
        return db.session.query(Products).filter(Products.name.ilike(name)).first()

    def select_product_by_id(self, id: int):
        return db.session.query(Products).filter(Products.id == id).first()
    
    def select_products_by_name(self, name: str):
        return db.session.query(Products).filter(Products.name.ilike(f"%{name}%")).all()
