from flask_restx import Namespace
from app import Resource,ns
from flask import request
from permissions.service import Permissions
from permissions.api_model import permission_model

permission = Permissions()

@ns.route('/permissions', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Permission(Resource):
    
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5},
    })
    @ns.response(200, "success")
    def get(self):
        if request.method == "GET":
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            return permission.permissions(page,per_page)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(permission_model)
    def post(self):
        if request.method=='POST':
            return permission.create_permissions(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
