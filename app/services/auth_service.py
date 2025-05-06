import bcrypt
from app.infraDB.repositories.users_repository import UsersRepository
from app.services.jwt_service import generate_jwt

def authenticate_user(email: str, senha: str):
    repo = UsersRepository()
    user = repo.select_user_by_email(email=email)

    if not user or not bcrypt.checkpw(senha.encode(), user.password_hash.encode()):
        return None

    token = generate_jwt(user)
    return token, user

