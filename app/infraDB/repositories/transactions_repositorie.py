from app.infraDB.models.transactions import Transactions, TransactionType
from app.infraDB.config.connection import db
class TransactionsRepository:
    def insert_transaction(self, product_id, type, quantity, blockchain_hash, user_id):
        data_insert = Transactions(
            product_id=product_id,
            type=type,
            quantity=quantity,
            blockchain_hash=blockchain_hash,
            user_id=user_id
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

    def select_transaction_by_id(self, transaction_id: int):
        data = db.session.query(Transactions).filter_by(id=transaction_id).first()
        return data

    def select_transactions_by_user(self, user_id: int):
        return db.session.query(Transactions).filter(Transactions.user_id == user_id).all()
