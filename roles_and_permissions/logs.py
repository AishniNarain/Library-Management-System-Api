from app import client
import datetime

database = client["library"]
roles_permissions_logs_collection = database["roles_permissions_logs"]

def log_roles_permissions_action(action, status, message=None, data=None):
    log_entry = {
        "action": action,
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.datetime.now()
    }
    
    roles_permissions_logs_collection.insert_one(log_entry)