#Defining different models

from .extensions import db
from datetime import date

class User(db.Model):
    __tablename__ = 'users'
    
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique = True, nullable= False,index=True)
    email = db.Column(db.String(100), unique= True, nullable= False,index=True)
    password = db.Column(db.String(50), nullable= False)
    registration_date = db.Column(db.DateTime)
    login_date = db.Column(db.DateTime)
    block_status = db.Column(db.Boolean)
    created_by = db.Column(db.Integer)
    relation = db.relationship('RolesandPermissions', backref="res", lazy=True, cascade="all, delete")
    students = db.relationship('Borrow', backref="user",cascade="all, delete")
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'registration_date': self.registration_date,
            'login_date': self.login_date,
            'block_status': self.block_status,
            'created_by': self.created_by
        }
        
class Role(db.Model):
    __tablename__ = 'roles'
    
    id =db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50),unique = True, nullable= False)
    
    def json(self):
        return {
            'id': self.id,
            'role_name': self.role_name
        }
        
class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id =db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(50),unique = True)
    
    def json(self):
        return {
            'id': self.id,
            'permission_name': self.permission_name
        }

class RolesandPermissions(db.Model):
    __tablename__ = 'user_roles_and_permissions'
    
    id = db.Column(db.Integer, primary_key= True)
    user_id =db.Column(db.Integer, db.ForeignKey("users.id"),index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    permission_ids = db.Column(db.String(100))
    
    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'permission_ids': self.permission_ids
        }
        
class Books(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50), nullable = False)
    publisher = db.Column(db.String(50), nullable = False)
    total_copies = db.Column(db.Integer, default=0)
    available_copies = db.Column(db.Integer, default=0)
    added_on = db.Column(db.Date)
    updated_on = db.Column(db.Date)
    borrower = db.relationship('Borrow', backref="book",cascade="all, delete")
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'total_copies': self.total_copies,
            'available_copies':self.available_copies,
            'added_on': self.added_on
    }
        
class Borrow(db.Model):
    __tablename__ = 'borrow_books'
    
    id = db.Column(db.Integer, primary_key = True)
    issue_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    issued_by = db.Column(db.Integer)
    fine = db.Column(db.Integer, default = 0)
    fine_days = db.Column(db.Integer, default = 0)
    status = db.Column(db.String(100))
    expected_return_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    books_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    
    def json(self):
        return {
            'id': self.id,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'issued_by': self.issued_by,
            'status': self.status,
            'expected_return_date':self.expected_return_date,
            'return_date': self.return_date,
            'student_id': self.student_id,
            'book_id': self.books_id
    }
        
class TokenBlockList(db.Model):
    __tablename__ = 'block_list'
    id = db.Column(db.Integer, primary_key= True)
    jti = db.Column(db.String(100), nullable= True)
    created_at = db.Column(db.DateTime, default=date.today)
    
    def json(self):
        return {
            'id': self.id,
            'jti':self.jti,
            'created_at': self.created_at
    }
