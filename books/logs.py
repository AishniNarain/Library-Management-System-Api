from app import client
import datetime

database = client["library"]
books_logs_collection = database["books_logs"]

def log_books_action(action, status, message=None, data=None):
    log_entry = {
        "action": action,
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.datetime.now()
    }
    
    books_logs_collection.insert_one(log_entry)