from flask_restx import fields
from ..app import api

role_model = api.model('Roles', {
    'role_name':fields.String(description="Role name")
    })