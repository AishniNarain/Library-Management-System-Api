from flask import make_response, jsonify,request
from extensions import db
from models import User,TokenBlockList,Role,RolesandPermissions,Borrow
from datetime import date,datetime
from flask_jwt_extended import create_access_token,create_refresh_token,current_user,get_jwt,jwt_required
from middleware import role, roles_required, access_required
from schemas import LoginSchema, RegisterSchema
from users.logs import log_action

#Defining all methods for users service
class Users:
    #defining the interface
    def __init__(self):
        pass
    
    @staticmethod
    def create():
        return Users()
    
    @jwt_required()
    @access_required(['Admin','Librarian'],['1'])
    def register_user(self,data):
        data = request.get_json()
        errors = RegisterSchema().validate(data)
        if errors:
            log_action("register_user", "failure", "Validation errors", current_user.id, errors)
            return errors, 422
            
        existing_email = User.query.filter_by(email=data['email']).first()
        existing_user = User.query.filter_by(username=data['username']).first()
        
        if existing_user:
            message = "Username already exists. Choose a different username"
            log_action("register_user", "failure", message, current_user.id, {"username": data['username']})
            response = make_response(jsonify({"message": message}))
            return response
        if existing_email:
            message = "Email already exists. Choose a different email address"
            log_action("register_user", "failure", message, current_user.id, {"email": data['email']})
            response = make_response(jsonify({"message": message}))
            return response
            
        user = User(username = data['username'], email = data['email'], password = data['password'], registration_date = date.today(), block_status = 0,created_by = current_user.id)
        db.session.add(user)
        db.session.commit()
        
        log_action("register_user", "success", "User created successfully", current_user.id, {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'registration_date': user.registration_date.isoformat(),
            'block_status': user.block_status,
            'created_by': user.created_by
        })

        return make_response(jsonify({'msg':'Signup Successful! User Created Successfully!',
                    'data': {
                        'id': user.id,
                        'username':user.username,
                        'email': user.email,
                        'password': user.password,
                        'registration_date':user.registration_date,
                        'block_status': user.block_status,
                        'created_by':user.created_by
        }}))
        
    def login(self,data):
        data = request.get_json()
        errors = LoginSchema().validate(data)
        if errors:
            log_action("login", "failure", "Validation errors", current_user.id, errors)
            return errors, 422

        user = User.query.filter(((User.username == data['username_or_email']) | (User.email == data['username_or_email']))).first()
        password = User.query.filter(User.password == data['password']).first()
        
        if not (user and password):
            message = "Invalid credentials"
            log_action("login", "failure", message)
            
            return make_response(jsonify({"msg":message}))
        else:
            access_token = create_access_token(identity=data['username_or_email'],fresh= True)
            refresh_token = create_refresh_token(identity=data['username_or_email'])
            user.login_date = date.today()
            db.session.commit()
            
            log_action("login", "success", "Logged in Successfully!", current_user.id, {
                "token":{
                            "access_token":access_token,
                            "refresh_token":refresh_token
                        }
            })
            
            return make_response(jsonify({
                                "msg":"Logged in Successfully!",
                                "token":{
                                "access_token":access_token,
                                "refresh_token":refresh_token
                                }
                            }))

    @jwt_required(verify_type = False)
    def logout(self):
        jwt = get_jwt()
        jti = jwt['jti']
        
        block_list = TokenBlockList(jti=jti)
        db.session.add(block_list)
        db.session.commit()
        
        response = make_response(jsonify({'msg':'You have successfully logged out'}),200)
        return response
    
    @jwt_required(fresh=True)
    @roles_required(['Admin','Librarian','Student'])
    def user_profile(self):
        data = User.query.filter_by(id = current_user.id).first()
        if not data:
            return jsonify({"message":"User doesn't exist"})
        response = make_response({
                                'username': data.username,
                                'email': data.email,
                                'password': data.password,
                                'registration_date' : data.registration_date,
                            })
        return response
    
    @jwt_required()
    @access_required(['Admin','Librarian'],['2'])
    def get_users(self,id=None,username=None,email=None,registration_date=None):
        role_name = role()
        if id is not None:
            if role_name == 'Admin':
                if current_user.id == id:
                    response = make_response(jsonify({'message':'Invalid request'}))
                    return response
                else:
                    data = User.query.filter(User.id == id, User.block_status == False).first()
                    if not data:
                        response = make_response(jsonify({'message':'No data available'}))
                        return response
                    response = make_response({
                                            'id': data.id,
                                            'username': data.username,
                                            'email': data.email,
                                            'password': data.password,
                                            'registration_date': data.registration_date,
                                            'login_date': data.login_date,
                                            'block_status': data.block_status,
                                            'created_by': data.created_by})
                    return response
            else:
                data = User.query.filter(User.created_by == current_user.id, User.block_status == False).all()
                for info in data:
                    if (info.id == id):
                        return make_response({
                                            'id': info.id,
                                            'username': info.username,
                                            'email': info.email,
                                            'password': info.password,
                                            'registration_date': info.registration_date,
                                            'login_date': info.login_date,
                                            'block_status': info.block_status,
                                            'created_by': current_user.username})
                return make_response(jsonify({'message':'Invalid user details request'}))
        else:
            users_query = User.query
            filters = []
            if role_name == 'Admin':
                if username or email:
                    filters.append((User.username.ilike(f"%{username}%"))| (User.email == email))
                if registration_date:
                    filters.append(User.registration_date == datetime.strptime(registration_date, '%Y-%m-%d'))
                users_query = users_query.filter(*filters)
                data = users_query.filter(User.id != current_user.id, User.block_status == False).all()
                details = {}
                creator_ids = set([info.created_by for info in data])
                creators = User.query.filter(User.id.in_(creator_ids)).all()
                for creator in creators:
                    details[creator.id] = creator.username
                for info in data:
                    info.created_by = details.get(info.created_by)
                return make_response(jsonify({'data': [info.json() for info in data]}), 200)
            else:
                if username or email:
                    filters.append((User.username.ilike(f"%{username}%"))| (User.email == email))
                if registration_date:
                    filters.append(User.registration_date == datetime.strptime(registration_date, '%Y-%m-%d'))
                users_query = users_query.filter(*filters)
                data = users_query.filter(User.created_by == current_user.id,User.block_status == False).all()
                if not data:
                    return make_response(jsonify({'msg':'No users available'}))
                for info in data:
                    info.created_by = current_user.username
                return make_response(jsonify({'data':[info.json() for info in data]}), 200)

    @jwt_required()
    @access_required(['Admin'],['3'])
    def update_user(self,id,data):
        if (current_user.id == id):
            return make_response(jsonify({'message':'Cannot update self'}))
        else:
            result = User.query.filter_by(id=id).first()
            if not result:
                return make_response(jsonify({"message":"User doesn't exist, cannot update"}))
            
            info = RolesandPermissions.query.filter_by(user_id = result.id).first()
            role = Role.query.filter_by(id = info.role_id).first()
            if role.role_name == 'Admin':
                return make_response(jsonify({'message':'Cannot update admin user'}))
            
            
            result.username = data['username']
            result.email = data['email']
            result.password = data['password']
            
            db.session.commit()
            return make_response(jsonify({'message':'User has been updated Successfully'}))
        
    @jwt_required()
    @access_required(['Admin','Librarian'],['4'])
    def delete_user(self,id):
        if (current_user.id == id):
            return make_response(jsonify({'message':'Cannot delete self'}))
        else:
            user = User.query.filter_by(id=id).first()
            if not user:
                return make_response(jsonify({'error':'User Not Found'}))
            else:
                borrow_count = Borrow.query.filter((Borrow.student_id == id) & (Borrow.status !='Return Request Initiated')).count()
                if borrow_count>=1:
                    return make_response(jsonify({'message':'Cannot delete user'}))
            data1 = RolesandPermissions.query.filter_by(user_id = user.id).first()
            data2 = RolesandPermissions.query.filter_by(user_id = current_user.id).first()
            if data1:
                role1 = Role.query.filter_by(id = data1.role_id).first()
                if role1.role_name == 'Admin':
                    return make_response(jsonify({'message':f"Cannot delete {role1.role_name} user"}))
            if data2:
                role2 = Role.query.filter_by(id = data2.role_id).first()
                if role2.role_name == 'Librarian':
                    return make_response(jsonify({'message':f"Cannot delete {role2.role_name} user"}))
            
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'data':'User deleted successfully'}))
        
    @jwt_required()
    @access_required(['Admin','Librarian'],['5'])
    def block_user(self,id):
        if (current_user.id == id):
            return make_response(jsonify({'message':'Cannot block self'}))
        else:
            result = User.query.filter_by(id=id).first()
            if not result:
                return make_response(jsonify({"message":"User doesn't exist, cannot block"}))
            else:
                borrow_count = Borrow.query.filter_by(student_id = id).count()
                data2 = Borrow.query.filter((Borrow.student_id == id) and (Borrow.status != 'Return Request Initiated')).first()
                if borrow_count > 1 or data2:
                    return make_response(jsonify({'message':'Cannot block user'}))
            data1 = RolesandPermissions.query.filter_by(user_id = result.id).first()
            data2 = RolesandPermissions.query.filter_by(user_id = current_user.id).first()
            role1 = Role.query.filter_by(id = data1.role_id).first()
            role2 = Role.query.filter_by(id = data2.role_id).first()
            if role1.role_name == 'Admin':
                return make_response(jsonify({'message':f"Cannot block {role1.role_name} user"}))
            if role2.role_name == 'Librarian':
                return make_response(jsonify({'message':f"Cannot block {role2.role_name} user"}))
            result.block_status = True
            db.session.commit()
            return make_response(jsonify({'message': 'User blocked Successfully'}))
        
    @jwt_required()
    @access_required(['Admin','Librarian'],['6'])
    def unblock_user(self,id):
        if (current_user.id == id):
            return make_response(jsonify({'message':'Invalid request'}))
        else:
            result = User.query.filter_by(id=id).first()
            if not result:
                return make_response(jsonify({"message":"User doesn't exist, cannot unblock"}))

            result.block_status = False
            db.session.commit()
            return make_response(jsonify({'message': 'User has been unblocked'}))