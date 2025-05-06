from app.infraDB.repositories.users_repository import UsersRepository
from app.infraDB.models.users import PermissionType
from app.utils.security import hash_password

def create_user_service(data):
    repo = UsersRepository()
    
    existing_user = repo.select_user_by_email(data["email"])
    if existing_user:
        raise ValueError("User already exists")

    permission = PermissionType(data["permission"])
    hashed_pw = hash_password(data["password"])

    return repo.insert_user(data["name"], data["email"], hashed_pw, permission)

def get_all_users_service():
    repo = UsersRepository()
    return repo.select_all_users()

def get_user_by_id_service(id: int):
    repo = UsersRepository()
    user = repo.select_user_by_id(id)
    if not user:
        raise ValueError("User not found")
    return user

def update_user_service(id, data):
    repo = UsersRepository()

    if "password" in data:
        data["password_hash"] = hash_password(data["password"])
        del data["password"]

    user = repo.update_user(
        id=id,
        name=data.get("name"),
        email=data.get("email"),
        password_hash=data.get("password_hash"),
        permission=data.get("permission")
    )

    if not user:
        raise ValueError("User not found")
    
    return user

def delete_user_service(id):
    repo = UsersRepository()
    success = repo.delete_user(id)

    if not success:
        raise ValueError("User not found")
    
    return True
