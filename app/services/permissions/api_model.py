from flask_restx import fields
from app import api

permission_model = api.model('Permissions', {
    'permission_name':fields.String(description="Permission name")
    })