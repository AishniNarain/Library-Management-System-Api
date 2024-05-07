#Implementing middleware for authentication and authorization

from flask import request, make_response, jsonify
from functools import wraps
from flask_jwt_extended import current_user
from models import Role, RolesandPermissions

def role():
    user_id = current_user.id
    data = RolesandPermissions.query.filter_by(user_id = user_id).first()
    role = Role.query.filter_by(id = data.role_id).first()
    role_name = role.role_name
    return role_name

def permission():
    user_id = current_user.id
    data = RolesandPermissions.query.filter_by(user_id = user_id).first()
    user_permissions = data.permission_ids
    return user_permissions

def roles_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:
                role_name = role()
                if any(role in role_name for role in required_roles):
                    return func(*args, **kwargs)
                else:
                    return make_response(jsonify({"message":"Unauthorized to access this endpoint"}), 403)
            
        return wrapper
    return decorator

def access_required(required_roles,required_permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:
                role_name = role()
                permissions = permission()
                if any(role in role_name for role in required_roles) and any(permission in permissions.split(',') for permission in required_permissions):
                    return func(*args, **kwargs)
                else:
                    return make_response(jsonify({"message":"Unauthorized to access this endpoint"}), 403)
            
        return wrapper
    return decorator
