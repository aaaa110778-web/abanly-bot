from datetime import datetime

user_access = {}

def check_password(user_id):
    today = datetime.now().date()
    return user_access.get(user_id) == today

def set_password_for_today(user_id):
    today = datetime.now().date()
    user_access[user_id] = today