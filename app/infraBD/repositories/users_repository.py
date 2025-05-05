from app.infraBD.models.users import Users, PermissionType
from app.infraBD.config.connection import db
from datetime import datetime, timezone

class UsersRepository:
    def insert_user(self, name: str, email: str, password_hash: str, permission: PermissionType):
        data_insert = Users(
            name=name,
            email=email,
            password_hash=password_hash,
            permission=permission
        )

        db.session.add(data_insert)
        db.session.commit()
        return data_insert

    def update_user(self, id: int, name: str = None, email: str = None, password_hash: str = None, permission: PermissionType = None):
        user = db.session.query(Users).filter(Users.id == id).first()
        if not user:
            return None

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password_hash is not None:
            user.password_hash = password_hash
        if permission is not None:
            user.permission = permission

        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return user

    def delete_user(self, id: int):
        result = db.session.query(Users).filter(Users.id==id).delete()
        db.session.commit()
        
        return result > 0

    def select_all_users(self):
        return db.session.query(Users).all()
