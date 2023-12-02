from flask import Blueprint, jsonify, request
from Controllers.UserController import login_user
from middleware.verify_token import verify_jwt_token

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/login', methods=['POST'])
def login_route():
    return login_user()