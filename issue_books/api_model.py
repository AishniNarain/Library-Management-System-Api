from flask_restx import fields
from app import api

issuebooks_model = api.model('Issue Books', {
    'book_id':fields.Integer(description="Book id to be borrowed"),
    'student_id':fields.Integer(description="Student id")
    })