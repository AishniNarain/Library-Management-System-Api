#Defining schemas for validation of data

from extensions import ma
from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)
    
class RegisterSchema(Schema):
    username = fields.Str(required=True, validate= validate.Length(min=4, max=10))
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate= validate.Length(min=8, max=15))
    
class RoleSchema(Schema):
    role_name = fields.Str(required=True)
    
class PermissionSchema(Schema):
    permission_name = fields.Str(required=True)
    
class RolesandPermsSchema(Schema):
    role_id = fields.Integer(required=True)
    permission_ids = fields.Str(required=True)
    
class BooksSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    publisher = fields.Str(required=True)
    total_copies = fields.Integer(required=True)
    
class IssueBooksSchema(Schema):
    student_id = fields.Integer(required=True)
    book_id = fields.Integer(required=True)