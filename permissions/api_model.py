from flask_restx import fields
from app import api

permission_model = api.model('Permissions', {
    'id': fields.Integer(description="Permission id"),
    'permission_name':fields.String(description="Permission name")
    })