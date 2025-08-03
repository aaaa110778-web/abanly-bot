import yfinance as yf
import requests
from modules.utils import get_trend_levels, calculate_digital_levels, format_levels, fetch_news

def analyze_stock(symbol: str) -> str:
    data = yf.Ticker(symbol)
    hist = data.history(period="1y")

    if hist.empty:
        raise Exception("❌ لم يتم العثور على بيانات للسهم.")

    high_price = hist['High'].max()
    low_price = hist['Low'].min()
    current_price = hist['Close'][-1]

    digital_levels = calculate_digital_levels(high_price, low_price)
    nearest_levels = [lvl for lvl in digital_levels if abs(lvl - current_price) <= 1.5][:3]

    levels_text = format_levels(nearest_levels)
    news = fetch_news(symbol)

    return f"""📊 *تحليل رقمي وفني لسهم {symbol.upper()}*:

• أعلى ترند: {high_price:.2f}
• أدنى ترند: {low_price:.2f}
• السعر الحالي: {current_price:.2f}

🎯 أقرب 3 مستويات:
{levels_text}

📰 الأخبار المؤثرة:
{news if news else "لا توجد أخبار مهمة."}

📌 التوصية:
إذا استقر فوق {nearest_levels[0]:.2f} مع دعم المؤشر، فقد يواصل الصعود.
📉 وقف الخسارة: دون {nearest_levels[0] - 0.5:.2f}
"""