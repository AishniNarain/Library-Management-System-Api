from flask_restx import fields
from api import api

rolesandpermissions_model = api.model('Roles and Permissions', {
    'user_id':fields.Integer(description="User id"),
    'role_id':fields.Integer(description="Role id"),
    'permission_ids':fields.String(description="Permission ids' associated with roles for each user")
})