import json
import os
from datetime import datetime

AUTH_FILE = "authorized_users.json"
user_access = {}

def get_today_key():
    return str(datetime.now().date())

def load_authorized_users():
    """
    تحميل المستخدمين المفعلين من الملف.
    """
    global user_access
    today_key = get_today_key()
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            try:
                data = json.load(f)
                user_access = {int(k): v for k, v in data.items() if v == today_key}
            except json.JSONDecodeError:
                user_access = {}
    else:
        user_access = {}

def save_authorized_users():
    """
    حفظ المستخدمين في الملف.
    """
    with open(AUTH_FILE, "w") as f:
        json.dump(user_access, f)

def set_password_for_today(user_id):
    """
    حفظ تفويض المستخدم لليوم.
    """
    today = get_today_key()
    user_access[user_id] = today
    save_authorized_users()

def check_password(user_id):
    """
    التحقق من صلاحية المستخدم.
    """
    return user_access.get(user_id) == get_today_key()
