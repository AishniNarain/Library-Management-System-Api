from flask import make_response, jsonify,request
from extensions import db, mail
from models import User,TokenBlockList,Role,RolesandPermissions,Books,Borrow
from datetime import date,timedelta,datetime
from flask_jwt_extended import JWTManager,create_access_token, create_refresh_token, current_user, get_jwt,jwt_required
from flask_mail import Message
from middleware import role, roles_required, access_required
from schemas import IssueBooksSchema
from issue_books.logs import log_issue_books_action

class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

#defining Email Observer class
class EmailObserver:
    def __init__(self,mail):
        self.mail = mail
        
    def update(self,recipients,issue_date,due_date,status,message,):
        msg = Message('Notification',
                        sender = 'aishninarain2000@gmail.com',
                        recipients = recipients)
        msg.body = f"Notification : Issue Date: {issue_date}, Due Date :{due_date},Status : {status}, Message : {message},"
        self.mail.send(msg)
        
email_observer = EmailObserver(mail)

class Issue_Books(Subject):
    def __init__(self):
        super().__init__()
        
    @jwt_required()
    @access_required(['Librarian'],['11'])
    def issue_books(self,data):
        data = request.get_json()
        
        errors = IssueBooksSchema().validate(data)
        if errors:
            return errors, 422
                
        books_id = Books.query.filter_by(id = data['book_id']).first()
        issue_date = date.today()
        due_date = issue_date+timedelta(days=1)
        data1 = RolesandPermissions.query.filter_by(user_id = data['student_id']).first()
        data2 = Role.query.filter_by(role_name = 'Student').first()
        
        if not books_id:
            log_issue_books_action("issue_books","failure","Book does not exist")
            return make_response(jsonify({'message':'Book does not exist'}))
        elif books_id.total_copies == 0:
            log_issue_books_action("issue_books","failure","Book unavailable")
            return make_response(jsonify({'message':'Book unavailable'}))
        elif data1.role_id != data2.id:
            log_issue_books_action("issue_books","failure","Invalid student id")
            return make_response(jsonify({'message':'Invalid student id'}))
        else:
            existing_borrow = Borrow.query.filter_by(student_id=data['student_id'], books_id=data['book_id']).first()
            if existing_borrow and not existing_borrow.status == 'Returned':
                log_issue_books_action("issue_books","failure","Student has already borrowed this book")
                return make_response(jsonify({'message': 'Student has already borrowed this book'}), 400)
            borrow_data = Borrow(issue_date = issue_date, due_date = due_date,issued_by = current_user.id,student_id = data['student_id'], books_id = data['book_id'])
            
            max_books = Borrow.query.filter((Borrow.books_id == data['book_id']) & (Borrow.status != 'Returned')).count()
            if max_books >= 2 and not(Borrow.status == 'Returned' or Borrow.status == 'Return Request Initiated'):
                log_issue_books_action("issue_books","failure","Sorry, student cannot borrow more than 2 books")
                return make_response(jsonify({'message':'Sorry, student cannot borrow more than 2 books'}))
                
            db.session.add(borrow_data)
            books_id.available_copies -= 1
            db.session.commit()

            log_issue_books_action("issue_books","success","Book has been issued successfully", current_user.id, {
                'data':{
                            'id': borrow_data.id,
                            'issue_date': borrow_data.issue_date,
                            'due_date': borrow_data.due_date,
                            'issued_by':borrow_data.issued_by,
                            'student_id': borrow_data.student_id,
                            'book_id': borrow_data.books_id
            }})
            return make_response(jsonify({'message':'Book has been issued successfully',
                                    'data':{
                                        'id': borrow_data.id,
                                        'issue_date': borrow_data.issue_date,
                                        'due_date': borrow_data.due_date,
                                        'issued_by':borrow_data.issued_by,
                                        'student_id': borrow_data.student_id,
                                        'book_id': borrow_data.books_id
                                    }}))
            
    @jwt_required()
    @access_required(['Librarian'],['13'])
    def initiate_return_request(self,id):
        data1 = Role.query.filter_by(role_name = 'Librarian').first()
        data2 = RolesandPermissions.query.filter_by(role_id = data1.id).all()
        for info1 in data2:
            id1 = info1.id
            data3 = Borrow.query.filter((Borrow.issued_by == id1) | (Borrow.issued_by != id1)).all()
            
            for info2 in data3:
                if(info2.id == id):
                    if (info2.status == 'Returned'):
                        log_issue_books_action("initiate_return_request","failure","Book has already been returned!")
                        return jsonify({'message':'Book has already been returned!'})
                    elif (info2.status == 'Return Request Initiated'):
                        log_issue_books_action("initiate_return_request","failure","Return Request has already been initiated!")
                        return jsonify({'message':'Return Request has already been initiated!'})
                    else:
                        data4 = Books.query.filter(Books.id == info2.books_id).first()
                        fine, days, current_date = calculate_fine(info2.due_date)
                        info2.fine = fine
                        info2.fine_days = days
                        info2.expected_return_date = current_date
                        info2.status = 'Return Request Initiated'
                        db.session.commit()
                        
                    log_issue_books_action("initiate_return_request","success","Return Request Initiated",current_user.id)
                    return jsonify({'message':'Return Request Initiated'})
                
            log_issue_books_action("initiate_return_request","failure","No data found")
            return jsonify({'message':'No data found'})
        
    @jwt_required()
    @access_required(['Librarian'],['13'])
    def return_book(self,id):
        data1 = Role.query.filter_by(role_name = 'Librarian').first()
        data2 = RolesandPermissions.query.filter_by(role_id = data1.id).all()
        for info1 in data2:
            id1 = info1.id
            data3 = Borrow.query.filter((Borrow.issued_by == id1) | (Borrow.issued_by != id1)).all()
            
            for info2 in data3:
                if(info2.id == id):
                    if (info2.status == 'Returned'):
                        log_issue_books_action("return_book","failure","Book has already been returned!")
                        return jsonify({'message':'Book has already been returned!'})
                    else:
                        data4 = Books.query.filter(Books.id == info2.books_id).first()
                        data4.available_copies = ((data4.available_copies)+1)
                        fine, days, current_date = calculate_fine(info2.due_date)
                        info2.return_date = current_date
                        info2.status = 'Returned'
                        db.session.commit()
                    log_issue_books_action("return_book","success","Book has been returned successfully!",current_user.id)
                    return jsonify({'message':'Book has been returned successfully!'})
            log_issue_books_action("return_book","failure","No data found")
            return jsonify({'message':'No data found'})

    @jwt_required()
    @access_required(['Librarian', 'Student'], ['12'])
    def issued_details(self, page, per_page, book_id, issue_date, status, student_id):
        borrow_query = Borrow.query
        if book_id or issue_date or status or student_id:
            borrow_query = borrow_query.filter((Borrow.books_id == book_id) |
                                            (Borrow.issue_date == issue_date) |
                                            (Borrow.status == status) |
                                            (Borrow.student_id == student_id))
        data = borrow_query.filter((Borrow.issued_by == current_user.id) |
                                (Borrow.student_id == current_user.id)).order_by(Borrow.id).paginate(
            page=page, per_page=per_page, error_out=False)
        response_data = []

        for info in data:
            data1 = Books.query.filter_by(id=info.books_id).first()
            data2 = User.query.filter_by(id=info.student_id).first()
            # email = data2.email
            data3 = User.query.filter_by(id=info.issued_by).first()
            fine, days, current_date = calculate_fine(info.due_date)

            if info.return_date is not None and info.status == 'Returned':
                message = f"Your total fine is Rs.{info.fine}"
            elif info.return_date is not None and info.status == 'Return Request Initiated':
                message = f"Your total fine is Rs.{fine}"
            elif fine == 0:
                info.status = 'No fine'
                db.session.commit()
                message = f"You have no fine till now"
            else:
                info.status = 'Fine Pending'
                db.session.commit()
                message = f"Your due date has exceeded and your fine is Rs.{fine} for {days} days"

            response_data.append({
                'id': info.id,
                'issue_date': info.issue_date.isoformat(),
                'due_date': info.due_date.isoformat(),
                'issued_by': data3.username,
                'status': info.status,
                'student_name': data2.username,
                'book_name': data1.title,
                'return_date': info.return_date,
                'message': message
                # 'email':email
            })

            # email_observer.update([email],info.issue_date,info.due_date,info.status,message)
        log_issue_books_action("issued_details","success","Details",current_user.id)
        return make_response(jsonify({'data': response_data}), 200)

    @jwt_required()
    @roles_required(['Librarian'])
    def get_all_students_issued_details(self,page,per_page,issue_date,status,student_id,book_id,issued_by):
        response_data = []
        data1 = Role.query.filter_by(role_name = 'Librarian').first()
        data2 = RolesandPermissions.query.filter_by(role_id = data1.id).all()
        for info in data2:
            id = info.id
            borrow_query = Borrow.query
            if issue_date or status or student_id or book_id or issued_by:
                borrow_query = borrow_query.filter((Borrow.issue_date == issue_date) | (Borrow.status == status) | (Borrow.student_id == student_id) | (Borrow.books_id == book_id) | (Borrow.issued_by == issued_by))
            data = borrow_query.filter((Borrow.issued_by == id) | (Borrow.issued_by != id)).order_by(Borrow.id).paginate(page=page,per_page=per_page,error_out=False)
            if data:
                for info in data:
                    data3 = Books.query.filter_by(id = info.books_id).first()
                    data4 = User.query.filter_by(id = info.student_id).first()
                    data5 = User.query.filter_by(id = info.issued_by).first()
                    
                    response_data.append({
                                        'id': info.id,
                                        'issue_date': info.issue_date,
                                        'due_date': info.due_date,
                                        'issued_by': data5.username,
                                        'status': info.status,
                                        'student_name': data4.username,
                                        'book_name': data3.title,
                                        'return_date':info.return_date
                                })
                log_issue_books_action("get_all_students_issued_details","success","Details",current_user.id)
                return make_response(jsonify({'data': response_data}), 200)
            else:
                log_issue_books_action("get_all_students_issued_details","failure","No data found")
                return make_response({'message':'No data found'})
            
    @jwt_required()
    @access_required(['Librarian','Student'],['14'])
    def issued_details_history(self,page,per_page,book_id,issue_date,student_id,issued_by):
        borrow_query = Borrow.query
        if book_id or issue_date or student_id or issued_by:
            borrow_query = borrow_query.filter((Borrow.books_id == book_id) | (Borrow.issue_date == issue_date) | (Borrow.student_id == student_id) | (Borrow.issued_by == issued_by))
        data = borrow_query.filter((Borrow.issued_by == current_user.id) | (Borrow.student_id == current_user.id)).order_by(Borrow.id).paginate(page=page,per_page=per_page,error_out=False)
        response_data = []
        
        for info in data:
            data1 = Books.query.filter_by(id = info.books_id).first()
            data2 = User.query.filter_by(id = info.student_id).first()
            data3 = User.query.filter_by(id = info.issued_by).first()
            if info.status == 'Returned':
                response_data.append({
                                    'id': info.id,
                                    'issue_date': info.issue_date,
                                    'due_date': info.due_date,
                                    'issued_by': data3.username,
                                    'status': info.status,
                                    'student_name': data2.username,
                                    'book_name': data1.title,
                                    'return_date':info.return_date,
                                    'fine':info.fine,
                                    'fine_days':info.fine_days
                                })
        log_issue_books_action("issued_details_history","success")
        return make_response(jsonify({'data': response_data}), 200)

    # @jwt_required()
    # @access_required(['Librarian'],['15'])
    # def send_emails(self,student_id):
    #     student_id = request.get_json()
        
    #     info = Borrow.query.filter_by(student_id = student_id).first()
    #     if not info:
    #         return make_response(jsonify({'msg':'U'}))
        
    #     return make_response(jsonify({'msg':'Yes'}))

def calculate_fine(due_date):
    current_date = date.today()
    if current_date < due_date:
        fine= 0
        days=0
    else:
        days = (current_date-due_date).days
        fine = (days*10)
    return fine, days,current_date

