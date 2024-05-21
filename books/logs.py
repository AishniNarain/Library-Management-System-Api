from app import client
import datetime

database = client["library"]
logs_collection = database["books_logs"]

def log_books_action(action, status, message, data=None):
    log_entry = {
        "action": action,
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.datetime.now()
    }
    
    logs_collection.insert_one(log_entry)