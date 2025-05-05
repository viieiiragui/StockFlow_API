from flask import Blueprint, request
from app.controllers.auth_controller import user_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return user_login(request.json)
