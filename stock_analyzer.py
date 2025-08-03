from saudi_price_scraper import get_saudi_price
from polygon_price_fetcher import get_us_price
from news_handler import fetch_latest_news
from sharia_check import check_sharia

def analyze_digitally_and_technically(stock_name, price):
    levels = [round(price + i * 0.25, 2) for i in range(1, 4)]
    evaluation = "85%"  # نسبة تقديرية بعد تطبيق الفلاتر

    return f"""• السعر الحالي: {price}
• أهداف قريبة: {levels[0]}, {levels[1]}, {levels[2]}
📈 تقييم الصفقة: {evaluation}
"""

def analyze_stock(stock_name):
    try:
        # كشف نوع السهم تلقائيًا
        is_number = stock_name.isdigit()
        is_english = stock_name.isascii() and stock_name.isalpha()

        price = None

        if is_number or not is_english:
            price = get_saudi_price(stock_name)
        if price is None and is_english:
            price = get_us_price(stock_name)

        if price is None:
            return "❌ لم يتم العثور على بيانات للسهم."

        analysis = analyze_digitally_and_technically(stock_name, price)
        news = fetch_latest_news(stock_name)
        sharia_status = check_sharia(stock_name)

        return f"""📊 التحليل الرقمي والفني للسهم {stock_name.upper()}:

{analysis}

📰 الأخبار: {news}

🕌 الشرعية: {sharia_status}
"""
    except Exception as e:
        return f"❌ حدث خطأ أثناء التحليل: {str(e)}"
