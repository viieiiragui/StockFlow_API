"""
Products model module.

Defines the SQLAlchemy model for product entities, including fields for
identification, attributes, stock tracking, timestamps, and relationships.
"""

from sqlalchemy.orm import relationship
from app.infraDB.config.connection import db
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime


class Products(db.Model):
    """
    SQLAlchemy model for products.

    Attributes:
        id (int): Primary key, auto-incremented identifier.
        name (str): Name of the product (required).
        category (str): Category to which the product belongs (required).
        current_stock (int): Current available stock quantity (defaults to 0).
        code (str): Unique product code (required).
        created_at (datetime): UTC timestamp when the product was created.
        updated_at (datetime): UTC timestamp when the product was last updated.
        transactions (list[Transactions]): Back-reference to related transactions.
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    current_stock = Column(Integer, nullable=False, default=0)
    code = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship to Transactions model; allows accessing all transactions for this product
    transactions = relationship("Transactions", backref="product", lazy=True)