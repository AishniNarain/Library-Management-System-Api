from flask_restx import fields
from ..app import api

post_model = api.model('Create Books', {
    'title': fields.String(required=True),
    'author':fields.String(description="Author of the book"),
    'publisher':fields.String(description="Publisher of the book"),
    'total_copies':fields.Integer(description="Total copies of the book")
    })

put_model = api.model('Update Books', {
    'title': fields.String(description="Title of the book"),
    'author':fields.String(description="Author of the book"),
    'publisher':fields.String(description="Publisher of the book"),
    'total_copies':fields.Integer(description="Total copies of the book")
    })