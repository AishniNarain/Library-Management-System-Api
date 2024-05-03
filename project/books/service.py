from flask import make_response, jsonify,request
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db,Books
from middleware import access_required
from schemas import BooksSchema

class BookMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    
#Defining the book service with all methods
class Book(metaclass=BookMeta):
    
    @staticmethod
    def get_books_schema():
        if not hasattr(Book, "_books_schema_instance"):
            Book._books_schema_instance = BooksSchema()
        return Book._books_schema_instance
    
    @jwt_required(refresh=False)
    @access_required(['Admin','Librarian','Student','Guest'],['2'])
    def get_books_inventory(self,page,per_page,title,author,publisher):
        books_query = Books.query
        
        if title or author or publisher:
            books_query = books_query.filter((Books.title == title) | (Books.author == author) | (Books.publisher == publisher))
            
        data = books_query.order_by(Books.id.asc()).paginate(page=page,per_page=per_page,error_out=False)
    
        if not data:
            response = make_response(jsonify({'msg':'No books available'}))
        response = make_response(jsonify({'data':[info.json() for info in data]}), 200)
        
        return response
    
    @jwt_required()
    @access_required(['Admin'],['3'])
    def add_book_inventory(self,data):
        data = request.get_json()
        
        # Get singleton instance of BooksSchema
        books_schema = self.get_books_schema()
        
        errors = books_schema.validate(data)
        if errors:
            return errors, 422
        
        added_on = datetime.today()
        books = Books(title = data['title'], author = data['author'],publisher = data['publisher'], total_copies = data['total_copies'],available_copies = data['total_copies'],added_on = added_on)
        db.session.add(books)
        db.session.commit()
        response = make_response(jsonify({'msg':'Book Created Successfully!',
                    'data': {
                        'id':books.id,
                        'title': books.title,
                        'author': books.author,
                        'publisher': books.publisher,
                        'total_copies': books.total_copies,
                        'available_copies': books.available_copies,
                        'added_on': books.added_on
                    }}))
        
        return response
    
    @jwt_required()
    @access_required(['Librarian'],['4'])
    def update_book_inventory(self, id, data):
        result = Books.query.filter_by(id=id).first()
        if not result:
            response = jsonify({"message":"Book doesn't exist, cannot update"})

        result.title = data["title"]
        result.author = data["author"]
        result.publisher = data["publisher"]
        result.total_copies = data["total_copies"]

        result.updated_on = datetime.today()
        db.session.commit()

        response= make_response(jsonify({'message':'Book updated Successfully'}))
    
        return response
    
    @jwt_required()
    @access_required(['Admin'],['5'])
    def delete_book_inventory(self, id):
        books = Books.query.filter_by(id=id).first()
        
        if not books:
            return {'error':'Book Not Found'}
        db.session.delete(books)
        db.session.commit()
        
        response= make_response(jsonify({'data':'Book deleted successfully'}))
        
        return response
        