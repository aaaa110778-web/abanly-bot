from modules.utils import get_today_key

authorized_users = {}

def is_authorized(user_id: int, today_key: str) -> bool:
    return authorized_users.get(user_id) == today_key