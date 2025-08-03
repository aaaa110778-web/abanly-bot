import datetime
import requests

def get_today_key():
    return datetime.date.today().isoformat()

def calculate_digital_levels(high, low, parts=24):
    step = (high - low) / parts
    return [round(low + i * step, 2) for i in range(parts + 1)]

def format_levels(levels):
    return "\n".join([f"• {lvl:.2f}" for lvl in levels])

def fetch_password():
    return "123123"

def fetch_news(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey=YOUR_NEWSAPI_KEY"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        if not articles:
            return None
        return "\n".join([f"• {a['title']}" for a in articles[:2]])
    except:
        return None