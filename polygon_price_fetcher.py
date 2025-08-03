import requests
import yfinance as yf

API_KEY = "zDQMb2_DyR4mWtvr6LVQQEz01dFsvMFN"

def get_us_price(symbol):
    # ✅ المحاولة 1: من Polygon.io
    try:
        url = f"https://api.polygon.io/v2/last/trade/{symbol.upper()}?apiKey={API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data and 'p' in data['results']:
                return float(data['results']['p'])  # 'p' = price
        else:
            print(f"⚠️ Polygon API Error: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Polygon error: {e}")

    # ✅ المحاولة 2: من Yahoo Finance
    try:
        ticker = yf.Ticker(symbol)
        live_price = ticker.info.get("regularMarketPrice") or ticker.info.get("currentPrice")
        if live_price:
            return float(live_price)
    except Exception as e:
        print(f"⚠️ Yahoo Finance error: {e}")

    # ❌ فشل في كل المحاولات
    return None
