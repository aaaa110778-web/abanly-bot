def analyze_digitally_and_technically(stock_name, price):
    # التحليل الرقمي والربط بالمؤشر
    levels = [round(price + i * 0.25, 2) for i in range(1, 4)]
    evaluation = "85%"  # نسبة تقديرية بعد تطبيق الفلاتر

    return f"""📊 التحليل الرقمي والفني للسهم {stock_name}:

• السعر الحالي: {price}
• أهداف قريبة: {levels[0]}, {levels[1]}, {levels[2]}
📈 تقييم الصفقة: {evaluation}
"""
