from flask_restx import fields
from app import api

register_model = api.model('Register Users', {
    'username':fields.String(description="Username of the user"),
    'email':fields.String(description="Email of the user"),
    'password':fields.String(description="Password of the user"),
    })

login_model = api.model('Login Users', {
    'username_or_email':fields.String(description="Username or email of the user"),
    'password':fields.String(description="Password of the user"),
    })

update_model = api.model('Update Users', {
    'username':fields.String(description="Username of the user"),
    'email':fields.String(description="Email of the user"),
    })