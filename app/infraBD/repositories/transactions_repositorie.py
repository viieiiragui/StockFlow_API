from app.infraBD.models.transactions import Transactions, TransactionType
from app.infraBD.config.connection import db

class TransactionsRepository:
    def insert_transaction(self, product_id: int, type: TransactionType, quantity: int, blockchain_hash: str):
        data_insert = Transactions(
            product_id=product_id,
            type=type,
            quantity=quantity,
            blockchain_hash=blockchain_hash
        )
        db.session.add(data_insert)
        db.session.commit()
        return data_insert

    def delete_transaction(self, id: int):
        result = db.session.query(Transactions).filter_by(id=id).delete()
        db.session.commit()
        return result > 0
    
    def select_all_transactions(self):
        data = db.session.query(Transactions).all()
        return data

    def select_transactions_by_product(self, product_id: int):
        data = db.session.query(Transactions).filter_by(product_id=product_id).all()
        return data