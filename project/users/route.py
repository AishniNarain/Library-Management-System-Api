from flask_restx import Namespace
from app import Resource
from api import ns
from flask import request
from .factory import UsersFactory
from .api_model import register_model,login_model,update_model

#defining an instance of the users using the UsersFactory
users_instance = UsersFactory.create_users()

@ns.route('/users/register', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Register(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(register_model)
    def post(self):
        if request.method=='POST':
            return users_instance.register_user(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/users/login', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        if request.method=='POST':
            return users_instance.login(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/users/logout', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Logout(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.response(200, "success")
    def get(self):
        if request.method == "GET":
            return users_instance.logout()
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/users/profile', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Profile(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.response(200, "success")
    def get(self):
        if request.method == "GET":
            return users_instance.user_profile()
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"

@ns.route('/users', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class GetAllUsers(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'username':{'in':'query','description':'Username','type':'string'},
        'email':{'in':'query','description':'Email','type':'string'},
        'registration_date': {'in': 'query', 'description': 'Registration date','type':'string','format': 'date'}
    })
    @ns.response(200, "success")
    def get(self):
        if request.method == "GET":
            username = request.args.get('username',type=str)
            email = request.args.get('email',type=str)
            registration_date = request.args.get('registration_date')
            return users_instance.get_users(username, email,registration_date)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"

@ns.route('/users/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class GetUsersById(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.response(200, "success")
    def get(self,id):
        if request.method == "GET":
            return users_instance.get_users(id)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(update_model)
    def put(self,id):
        if request.method=='PUT':
            return users_instance.update_user(id, request.json)
        message = "This method is not allowed here please use the 'PUT' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
    @ns.doc(security = [{'Bearer':[]}])
    def delete(self,id):
        if request.method == 'DELETE':
            return users_instance.delete_user(id)
        message = "This method is not allowed here please use the 'DELETE' method"
        return f"data="", error={True}, code='405', message={message}, details=''"


@ns.route('/users/block/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class BlockUsers(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    def patch(self,id):
        if request.method=='PATCH':
            return users_instance.block_user(id)
        message = "This method is not allowed here please use the 'PATCH' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
@ns.route('/users/unblock/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class UnblockUsers(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    def patch(self,id):
        if request.method=='PATCH':
            return users_instance.unblock_user(id)
        message = "This method is not allowed here please use the 'PATCH' method"
        return f"data="", error={True}, code='405', message={message}, details=''"