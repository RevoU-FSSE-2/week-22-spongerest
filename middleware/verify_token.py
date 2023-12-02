from multiprocessing import process
from flask import app, request, jsonify
import jwt
from functools import wraps
import os

def verify_jwt_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            print(f"Received token: {token}")
            if not token:
                return jsonify({'message': 'Unauthorized, token not provided'}), 401

            token = token.split(" ")[1] if token.startswith("Bearer ") else token

            decoded_token = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])

            if not decoded_token or 'id' not in decoded_token or 'role' not in decoded_token:
                return jsonify({'message': 'Invalid token structure'}), 401

            request.user = decoded_token

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return jsonify({'message': f'Invalid token: {str(e)}'}), 401
        except Exception as e:
            print(f"Error decoding token: {e}")
            return jsonify({'message': f'Error decoding token: {str(e)}'}), 401

        return func(*args, **kwargs)

    return wrapper

def authorize_admin_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(request, 'user') and request.user.get('role') == 'admin':
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized: Admin role required'}), 403

    return wrapper