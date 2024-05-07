from flask import make_response, jsonify,request
from ..models import db, RolesandPermissions,User,Role,Permission
from flask_jwt_extended import jwt_required
from ..middleware import roles_required
from ..schemas import RolesandPermsSchema

#Defining all methods of Roles and Permissions service
class RolesandPermission():
    @jwt_required()
    @roles_required(['Admin'])
    def get_user_roles_and_permissions(self,page,per_page,role_id,permission_ids):
        filters = []
        result_query = RolesandPermissions.query
        
        if role_id:
            filters.append(RolesandPermissions.role_id == role_id)
        if permission_ids:
            filters.append(RolesandPermissions.permission_ids.ilike(f"%{permission_ids}%"))
        result_query = result_query.filter(*filters)
        data = result_query.order_by(RolesandPermissions.id.asc()).paginate(page=page,per_page=per_page,error_out=False)
        
        if not data:
            response = make_response(jsonify({'msg':'No data available'}))
        
        response = make_response(jsonify({'data':[info.json() for info in data]}), 200)
        return response
    
    @jwt_required()
    @roles_required(['Admin'])
    def create_userrolesandpermissions(self,id,data):
        info = User.query.filter_by(id=id).first()
        if not info:
            response = jsonify({'msg':'No user found, cannot add details'})
        else:
            data = request.get_json()
            if not data:
                errors = RolesandPermsSchema().validate(data)
                if errors:
                    return errors, 422
            
            user_roles_and_permissions = RolesandPermissions(role_id = data['role_id'],permission_ids = data['permission_ids'])
            
            role = Role.query.filter_by(id = data['role_id']).all()
            permission= Permission.query.filter_by(id = data['permission_ids']).all()
            if not role :
                response = jsonify({'msg':'No role id found'})
            elif not permission :
                response = jsonify({'msg':'No permission ids found'})
            else:
                user_roles_and_permissions.res = info
        
                db.session.add(user_roles_and_permissions)
                db.session.commit()
                response = jsonify({'msg':'User Roles and Permissions Created Successfully!',
                        'data': {
                            'id':user_roles_and_permissions.id,
                            'user_id': user_roles_and_permissions.res.id,
                            'role_id':user_roles_and_permissions.role_id,
                            'permission_ids':user_roles_and_permissions.permission_ids
                        }})
        return response
