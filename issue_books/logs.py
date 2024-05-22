from app import client
import datetime

database = client["library"]
issue_books_logs_collection = database["issue_books_logs"]

def log_issue_books_action(action, status, message=None, user_id=None, data=None):
    log_entry = {
        "action": action,
        "status": status,
        "message": message,
        "user_id": user_id,
        "data": data,
        "timestamp": datetime.datetime.now()
    }
    
    issue_books_logs_collection.insert_one(log_entry)