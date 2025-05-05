from sqlalchemy.orm import relationship
from app.infraBD.config.connection import db
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime

class Products(db.Model):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    current_stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    transactions = relationship("Transactions", backref="product", lazy=True)
