import requests

API_KEY = "zDQMb2_DyR4mWtvr6LVQQEz01dFsvMFN"

def get_us_price(symbol):
    try:
        url = f"https://api.polygon.io/v1/last/stocks/{symbol}?apiKey={API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['last']['price'])
    except:
        return None