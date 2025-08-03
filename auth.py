auth_log = {}
def is_authenticated(user_id, date): return auth_log.get((user_id, date), False)
def save_access(user_id, date, status): auth_log[(user_id, date)] = status
