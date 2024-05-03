from flask_restx import fields
from api import api

role_model = api.model('Roles', {
    'role_name':fields.String(description="Role name")
    })