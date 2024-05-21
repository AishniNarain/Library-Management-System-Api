from flask import make_response, jsonify,request
from extensions import db
from models import Role
from flask_jwt_extended import jwt_required
from middleware import roles_required
from schemas import RoleSchema
from roles.logs import log_roles_action

#Defining the roles service with all methods
class Roles():
    
    @jwt_required()
    @roles_required(['Admin'])
    def roles(self,page,per_page):
        data = Role.query.order_by(Role.id.asc()).paginate(page=page,per_page=per_page,error_out=False)
        
        if not data:
            log_roles_action("roles","failure",'No roles available')
            response = make_response(jsonify({'msg':'No roles available'}))
        
        log_roles_action("roles","success","Details",{
            'data':[info.json() for info in data]
        })
        response = make_response(jsonify({'data':[info.json() for info in data]}), 200)
        return response
    
    @jwt_required()
    @roles_required(['Admin'])
    def create_roles(self,data):
        data = request.get_json()
        
        if not data:
            errors = RoleSchema().validate(data)
            if errors:
                log_roles_action("create_roles", "failure", "Validation errors",errors)
                return errors, 422
        
        roles = Role(role_name = data['role_name'])
        db.session.add(roles)
        db.session.commit()
        
        log_roles_action("create_roles", "success",'Roles Created Successfully!',{
            'data': {
                        'id':roles.id,
                        'role_name': roles.role_name,
                    }
            })
        
        response = make_response(jsonify({'msg':'Roles Created Successfully!',
                        'data': {
                            'id':roles.id,
                            'role_name': roles.role_name,
                        }}))
        return response