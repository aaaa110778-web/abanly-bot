import json
import os
from modules.utils import get_today_key

AUTH_FILE = "authorized_users.json"
authorized_users = {}

def load_authorized_users():
    """
    تحميل المستخدمين المفعلين من الملف إذا كان موجود.
    فقط المستخدمين اللي مفتاحهم يطابق اليوم الحالي يتم الاحتفاظ بهم.
    """
    global authorized_users
    today_key = get_today_key()

    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            try:
                data = json.load(f)
                # تصفية المستخدمين بناءً على تاريخ اليوم فقط
                authorized_users = {int(k): v for k, v in data.items() if v == today_key}
            except json.JSONDecodeError:
                authorized_users = {}
    else:
        authorized_users = {}

def save_authorized_users():
    """
    حفظ المستخدمين المفعلين في الملف.
    """
    with open(AUTH_FILE, "w") as f:
        json.dump(authorized_users, f)

def authorize_user(user_id: int):
    """
    تفعيل المستخدم وتخزينه.
    """
    today_key = get_today_key()
    authorized_users[user_id] = today_key
    save_authorized_users()

def is_authorized(user_id: int) -> bool:
    """
    التحقق من صلاحية المستخدم لليوم.
    """
    return authorized_users.get(user_id) == get_today_key()
