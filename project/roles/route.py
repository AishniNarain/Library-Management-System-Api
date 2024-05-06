from flask_restx import Namespace
from ..app import Resource,ns
from flask import request
from .service import Roles
from .api_model import role_model

role = Roles()

@ns.route('/roles', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Role(Resource):
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
            return role.roles(page,per_page)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(role_model)
    def post(self):
        if request.method=='POST':
            return role.create_roles(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
