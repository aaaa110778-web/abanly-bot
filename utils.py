from saudi_price_scraper import get_saudi_price
from polygon_price_fetcher import get_us_price
from stock_analyzer import analyze_digitally_and_technically
from news_handler import fetch_latest_news
from sharia_check import check_sharia

def analyze_stock(stock_name: str) -> str:
    try:
        # تحديد نوع السوق تلقائيًا
        is_number = stock_name.isdigit()
        is_english = stock_name.isascii() and stock_name.isalpha()

        price = None

        if is_number or not is_english:
            # سهم سعودي: إما برمز أو اسم عربي
            price = get_saudi_price(stock_name)
        if price is None and is_english:
            # سهم أمريكي
            price = get_us_price(stock_name)

        if price is None:
            return "❌ لم يتم العثور على بيانات للسهم."

        analysis = analyze_digitally_and_technically(stock_name, price)
        news = fetch_latest_news(stock_name)
        sharia_status = check_sharia(stock_name)

        return f"""📊 تحليل السهم {stock_name.upper()}:

{analysis}

📰 الأخبار: {news}

🕌 الشرعية: {sharia_status}
"""

    except Exception as e:
        return f"❌ حدث خطأ أثناء التحليل: {str(e)}"
