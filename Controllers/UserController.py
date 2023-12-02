from multiprocessing import process
import os
from flask import app, make_response, request, jsonify
import bcrypt
from flask_cors import CORS
import jwt
from models.User import User
from bson import ObjectId



def register_user():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if len(password) < 5:
            return jsonify({'error': 'Password must be at least 5 characters long'}), 400

        existing_user = User.objects(email=email).first()

        if existing_user:
            return jsonify({'error': 'Email is already in use'}), 400

        salt_rounds = 10
        salt = bcrypt.gensalt(salt_rounds)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        user = User(name=name, email=email, password=hashed_password, role=role)
        saved_user = user.save()

        return jsonify({'message': 'Registration successful', 'user': saved_user.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def login_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if role == 'user':
            user = User.objects(email=email, role='user').first()
        elif role == 'admin':
            user = User.objects(email=email, role='admin').first()
        else:
            return jsonify({'message': 'Invalid role specified'}), 400

        if not user:
            return jsonify({'message': f'{role.capitalize()} Not Found'}), 404

        is_matched = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

        if not is_matched or email != user.email or role != user.role:
            return jsonify({'message': 'Invalid credentials or status unknown'}), 401

        if user.status != "active":
            return jsonify({'message': 'Account is inactive'}), 401

        user_res = user.to_dict()
        if 'password' in user_res:
            del user_res['password']

        token = jwt.encode({'id': str(user.id), 'role': role}, os.environ.get('SECRET_KEY'), algorithm='HS256')

        response_data = {'user': user_res, 'token': token}
        response = jsonify(response_data)
        response.set_cookie('token', token, httponly=True)

        # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        # response.headers['Access-Control-Allow-Credentials'] = 'true'
        # response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        # response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST, GET, PUT, DELETE'

        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_users():
    try:
        users = User.objects()
        users_list = [user.to_dict() for user in users]

        response_data = {'users': users_list}
        response = make_response(jsonify(response_data))

        response.headers.add('Access-Control-Allow-Credentials', 'true')

        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_user(user_id):
    try:
        user_data = request.json
        user = User.objects(id=user_id).first()

        if user:
            allowed_fields = ['status', 'role']
            for field in allowed_fields:
                if field in user_data:
                    setattr(user, field, user_data[field])

            user.save()

            return jsonify({'user': user.to_dict()}), 201
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user(user_id):
    try:
        user = User.objects(id=user_id).first()

        if user:
            return jsonify({'user': user}), 201
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_user(user_id):
    try:
        deleted_user = User.objects(id=user_id).first()

        if deleted_user:
            deleted_user.delete()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500