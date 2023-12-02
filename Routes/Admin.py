from flask import Blueprint, jsonify
from Controllers.UserController import login_user, get_users, update_user, get_user, delete_user
from middleware.verify_token import verify_jwt_token, authorize_admin_access

admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route('/users', methods=['GET'])
@verify_jwt_token
@authorize_admin_access
def get_users_route():
    return get_users()


@admin_routes.route('/users/<id>', methods=['PUT'])
@verify_jwt_token
@authorize_admin_access
def update_user_route(id):
    return update_user(id)


@admin_routes.route('/users/<id>', methods=['DELETE'])
@verify_jwt_token
@authorize_admin_access
def delete_user_route(id):
    return delete_user(id)


@admin_routes.route('/<id>', methods=['GET'])
@verify_jwt_token
@authorize_admin_access
def get_user_route(id):
    return get_user(id)