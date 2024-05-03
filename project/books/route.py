from flask_restx import Resource,Namespace
from api import ns
from flask import request
from .service import Book
from .api_model import post_model,put_model

# ns = Namespace('books', description='Books related operations')

book = Book()

@ns.route('/books', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Book(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.doc(params={
        'title':{'in':'query','description':'Title of the book','type':'string'},
        'author':{'in':'query','description':'Author of the book','type':'string'},
        'publisher':{'in':'query','description':'Publisher of the book','type':'string'},
        'page': {'in': 'query', 'description': 'Page no','type':'int', 'default': 1},
        'per_page': {'in': 'query', 'description': 'Per page details','type':'int', 'default': 5}
    })
    @ns.response(200, "success")
    def get(self):
        if request.method == "GET":
            page = request.args.get('page',type=int)
            per_page = request.args.get('per_page',type=int)
            title = request.args.get('title',type=str)
            author = request.args.get('author',type=str)
            publisher = request.args.get('publisher',type=str)
            return book.get_books_inventory(page,per_page,title,author,publisher)
        message = "This method is not allowed here please use the 'GET' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
        
    
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(post_model)
    def post(self):
        if request.method=='POST':
            return book.add_book_inventory(request.json)
        message = "This method is not allowed here please use the 'POST' method"
        return f"data="", error={True}, code='405', message={message}, details=''"

@ns.route('/books/<int:id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class Book_UpdateandDelete(Resource):
    @ns.doc(security = [{'Bearer':[]}])
    @ns.expect(put_model)
    def put(self,id):
        if request.method=='PUT':
            return book.update_book_inventory(id, request.json)
        message = "This method is not allowed here please use the 'PUT' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    
    @ns.doc(security = [{'Bearer':[]}])
    def delete(self,id):
        if request.method == 'DELETE':
            return book.delete_book_inventory(id)
        message = "This method is not allowed here please use the 'DELETE' method"
        return f"data="", error={True}, code='405', message={message}, details=''"
    