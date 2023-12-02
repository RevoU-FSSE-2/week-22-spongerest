from flask import Blueprint, jsonify, request
from Controllers.TaskController import create_task, get_task, get_tasks, update_task, delete_task
from middleware.verify_token import verify_jwt_token

task_routes = Blueprint('task_routes', __name__)

@task_routes.before_request
@verify_jwt_token
def before_request():
    print("Before request")

@task_routes.route('/create', methods=['POST'])
@verify_jwt_token
def create_task_route():
    return create_task()

@task_routes.route('/update/<task_id>', methods=['PUT'])
@verify_jwt_token
def update_task_route(task_id):
    return update_task(task_id)

@task_routes.route('/<task_id>', methods=['GET'])
@verify_jwt_token
def get_task_route(task_id):
    return get_task(task_id)

@task_routes.route('/<task_id>', methods=['DELETE'])
@verify_jwt_token
def delete_task_route(task_id):
    return delete_task(task_id)

@task_routes.route('/', methods=['GET'])
@verify_jwt_token
def get_tasks_route():
    return get_tasks()