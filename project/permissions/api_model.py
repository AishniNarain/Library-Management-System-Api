from flask_restx import fields
from api import api

permission_model = api.model('Permissions', {
    'permission_name':fields.String(description="Permission name")
    })