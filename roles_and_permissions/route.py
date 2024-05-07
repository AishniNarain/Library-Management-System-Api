from app import Resource,ns
from flask import request
from service import RolesandPermission
from api_model import rolesandpermissions_model

roles_and_permissions = RolesandPermission()

@ns.route('/user_rolesandpermissions', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Get_RolesandPermissions(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5},
        'role_id': {'in': 'query', 'description': 'Role id','type':'int'},
        'permission_ids': {'in': 'query', 'description': 'Permission ids','type':'string'},
    })
    @ns.response(200, "success")
    def get(self):
        if request.method=='GET':
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            role_id = request.args.get('role_id',type=int)
            permission_ids = request.args.get('permission_ids',type=str)
            return roles_and_permissions.get_user_roles_and_permissions(page,per_page,role_id,permission_ids)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/user_rolesandpermissions/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Create_RolesandPermissions(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(rolesandpermissions_model)
    def post(self,id):
        if request.method=='POST':
            return roles_and_permissions.create_userrolesandpermissions(id, request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"