from sqlalchemy.orm import relationship
from app.infraDB.config.connection import db
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime

class Products(db.Model):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    current_stock = Column(Integer, nullable=False, default=0)
    code = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    transactions = relationship("Transactions", backref="product", lazy=True)
